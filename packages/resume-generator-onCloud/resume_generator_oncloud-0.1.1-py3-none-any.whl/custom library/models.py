from django.db import models
from django.contrib.auth.models import User

class Resume(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='resumes')
    full_name = models.CharField(max_length=255)
    email = models.EmailField()
    template = models.CharField(max_length=50, default='default_template')
    content = models.TextField(blank=True)  # Main resume content (HTML or plain text)
    extra_fields = models.JSONField(blank=True, null=True)  
    # Stores additional details specific to the chosen template (as JSON)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.full_name}'s Resume"


# Model for versioning the resume content
class ResumeVersion(models.Model):
    resume = models.ForeignKey(Resume, on_delete=models.CASCADE, related_name='versions')
    version_number = models.PositiveIntegerField()
    content = models.TextField(blank=True)  # Main content
    extra_fields = models.JSONField(blank=True, null=True)  # Extra fields from the editor
    updated_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Version {self.version_number} for {self.resume.full_name}"

