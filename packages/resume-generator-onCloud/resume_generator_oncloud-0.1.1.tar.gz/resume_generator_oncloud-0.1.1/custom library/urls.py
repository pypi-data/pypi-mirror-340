from django.urls import path
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
from .views import (
    GetCSRFTokenView,  # Dedicated CSRF endpoint
    ResumeWelcomeView,
    RegistrationView,
    LoginView,
    LogoutView,
    ResumeListCreateView,
    ResumeRetrieveUpdateDestroyView,
    GeneratePDFView,
    ResumeVersionListView,
    ResumeRollbackView,
)

urlpatterns = [
    # CSRF endpoint
    path('api/get-csrf-token/', GetCSRFTokenView.as_view(), name='get-csrf-token'),
     # Map the root URL to the welcome view so that accessing "/" returns a response.
    path('', ResumeWelcomeView.as_view(), name='root-welcome'),

    path('api/', ResumeWelcomeView.as_view(), name='api-welcome'),

    # Session-based auth endpoints
    path('api/auth/register/', RegistrationView.as_view(), name='api-register'),
    path('api/auth/login/', LoginView.as_view(), name='api-login'),
    path('api/auth/logout/', LogoutView.as_view(), name='api-logout'),

    # JWT endpoints (optional)
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

    # Resume endpoints
    path('api/resume/', ResumeListCreateView.as_view(), name='resume-list-create'),
    path('api/resume/<int:pk>/', ResumeRetrieveUpdateDestroyView.as_view(), name='resume-detail'),

    # Version & Rollback endpoints
    path('api/resume/<int:pk>/versions/', ResumeVersionListView.as_view(), name='resume-versions'),
    path('api/resume/<int:pk>/rollback/<int:version_number>/', ResumeRollbackView.as_view(), name='resume-rollback'),

    # PDF Generation
    path('api/generate-pdf/', GeneratePDFView.as_view(), name='generate-pdf'),
]
