import uuid
import json
import datetime
import logging
import os

from django.conf import settings
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.password_validation import validate_password
from rest_framework import status, generics, permissions
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.exceptions import ValidationError, NotFound

from .dynamo_models import ResumeDynamo, VersionItem
from .serializers import ResumeSerializer
from .djangoService import generate_pdf, upload_file_to_s3

logger = logging.getLogger(__name__)

# ---------------- CSRF Token ----------------
class GetCSRFTokenView(APIView):
    permission_classes = [permissions.AllowAny]
    def get(self, request):
        from django.middleware.csrf import get_token
        token = get_token(request)
        return Response({"detail": "CSRF cookie set", "csrftoken": token})

# ---------------- Authentication ----------------
class RegistrationView(APIView):
    permission_classes = [permissions.AllowAny]
    def post(self, request):
        data = request.data
        username, password, email = data.get('username'), data.get('password'), data.get('email')
        if not username or not password or not email:
            return Response({"error": "Username, password, and email are required."}, status=400)
        if User.objects.filter(username=username).exists():
            return Response({"error": "Username already exists."}, status=400)
        try:
            validate_password(password)
        except ValidationError as e:
            return Response({"error": e.messages}, status=400)
        User.objects.create_user(username=username, password=password, email=email)
        return Response({"message": "User registered successfully."}, status=201)

class LoginView(APIView):
    permission_classes = [permissions.AllowAny]
    def post(self, request):
        user = authenticate(request, **request.data)
        if user:
            login(request, user)
            return Response({"message": "Login successful", "username": user.username})
        return Response({"error": "Invalid credentials"}, status=401)

class LogoutView(APIView):
    def post(self, request):
        logout(request)
        return Response({"message": "Logged out successfully"})

# ---------------- Resume CRUD (DynamoDB) ----------------
class ResumeListCreateView(generics.ListCreateAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = ResumeSerializer

    def get_queryset(self):
        # Fetch resumes for the current user from DynamoDB
        user_id = str(self.request.user.id)
        resumes = ResumeDynamo.scan(user_id=user_id)  # Adjust based on your DynamoDB setup
        return resumes

    def perform_create(self, serializer):
        # Custom logic to save to DynamoDB instead of a Django model
        data = serializer.validated_data
        new_id = str(uuid.uuid4())
        resume = ResumeDynamo(
            resume_id=new_id,
            user_id=str(self.request.user.id),
            content=data.get("content", ""),
            extra_fields=data.get("extra_fields", {}),
            versions=[]
        )
        resume.save()
        initial_version = VersionItem(
            version_number="1",
            content=resume.content,
            extra_fields=resume.extra_fields,
            updated_at=datetime.datetime.utcnow().isoformat()
        )
        resume.versions = [initial_version]
        resume.save()
        serializer.instance = resume  # Set the instance for the response

class ResumeRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = ResumeSerializer
    lookup_field = 'resume_id'

    def get_object(self):
        resume_id = self.kwargs.get('resume_id')
        try:
            resume = ResumeDynamo.get(resume_id)
            if resume.user_id != str(self.request.user.id):
                raise PermissionError("You do not have permission to access this resume.")
            return resume
        except ResumeDynamo.DoesNotExist:
            raise NotFound("Resume not found.")

    def perform_update(self, serializer):
        resume = self.get_object()
        data = serializer.validated_data
        resume.content = data.get("content", resume.content)
        resume.extra_fields = data.get("extra_fields", resume.extra_fields)
        resume.save()
        new_version = VersionItem(
            version_number=str(len(resume.versions or []) + 1),
            content=resume.content,
            extra_fields=resume.extra_fields,
            updated_at=datetime.datetime.utcnow().isoformat()
        )
        resume.versions.append(new_version)
        resume.save()
        serializer.instance = resume

    def perform_destroy(self, instance):
        instance.delete()

class ResumeVersionListView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, resume_id):
        try:
            resume = ResumeDynamo.get(resume_id)
            if resume.user_id != str(request.user.id):
                return Response({"error": "You do not have permission to access this resume."}, status=403)
            versions = [
                {
                    "version_number": v.version_number,
                    "content": v.content,
                    "extra_fields": v.extra_fields,
                    "updated_at": v.updated_at
                } for v in resume.versions or []
            ]
            return Response({"resume_id": resume_id, "versions": versions})
        except ResumeDynamo.DoesNotExist:
            return Response({"error": "Resume not found."}, status=404)

class ResumeRollbackView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, resume_id):
        version_number = request.data.get("version_number")
        if not version_number:
            return Response({"error": "Version number is required."}, status=400)

        try:
            resume = ResumeDynamo.get(resume_id)
            if resume.user_id != str(request.user.id):
                return Response({"error": "You do not have permission to access this resume."}, status=403)
        except ResumeDynamo.DoesNotExist:
            return Response({"error": "Resume not found."}, status=404)

        target = next((v for v in (resume.versions or []) if v.version_number == version_number), None)
        if not target:
            return Response({"error": "Version not found."}, status=404)
        if resume.content == target.content:
            return Response({"message": "Already at selected version."})

        resume.content = target.content
        resume.extra_fields = target.extra_fields
        resume.save()
        new_version = VersionItem(
            version_number=str(len(resume.versions) + 1),
            content=resume.content,
            extra_fields=resume.extra_fields,
            updated_at=datetime.datetime.utcnow().isoformat()
        )
        resume.versions.append(new_version)
        resume.save()
        return Response({"message": "Rollback successful.", "new_version": new_version.version_number})

# ---------------- PDF Generation + S3 Upload ----------------
class GeneratePDFView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        html = request.data.get('html_content')
        if not html:
            return Response({"error": "HTML content required."}, status=status.HTTP_400_BAD_REQUEST)

        # Step 1: Save HTML locally
        filename = f"resume_{uuid.uuid4()}.html"
        local_path = os.path.join(settings.BASE_DIR, filename)
        with open(local_path, 'w', encoding='utf-8') as f:
            f.write(html)

        # Step 2: Upload to S3 (trigger Lambda)
        s3_key = f"incoming-resumes/{request.user.id}/{filename}"
        success = upload_file_to_s3(local_path, settings.S3_BUCKET_NAME, s3_key)

        if not success:
            return Response({"error": "Failed to upload HTML to S3."}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        return Response({
            "message": "HTML uploaded successfully. PDF generation in progress.",
            "html_s3_key": s3_key
        }, status=status.HTTP_202_ACCEPTED)

# ---------------- Welcome View ----------------
class ResumeWelcomeView(APIView):
    """
    Simple view to welcome users or test the API.
    """
    def get(self, request):
        return Response({"message": "Welcome to the Resume API!"})