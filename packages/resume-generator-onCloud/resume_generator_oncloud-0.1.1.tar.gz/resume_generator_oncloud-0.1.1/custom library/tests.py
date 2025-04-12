from django.test import TestCase
from django.contrib.auth.models import User
from .models import Resume

class ResumeModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpass')
        self.resume = Resume.objects.create(user=self.user, full_name='Test User', email='test@example.com')

    def test_resume_str(self):
        self.assertEqual(str(self.resume), "Test User's Resume")
