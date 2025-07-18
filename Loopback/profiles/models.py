from django.db import models
# from users.models import User
from django.contrib.auth import get_user_model
from django.contrib.postgres.fields import JSONField

User = get_user_model()
# Mentor Model

class MentorProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='mentor_profile')
    google_credentials = models.JSONField(null=True, blank=True)
    username = models.CharField(max_length=255, blank=True, null=True)
    passport_image = models.ImageField(upload_to='passport_images/', blank=True, null=True)
    passport_image_url = models.URLField(blank=True, null=True)
    company = models.CharField(max_length=255, blank=True, null=True)
    job_title = models.CharField(max_length=255, blank=True, null=True)
    industry = models.CharField(max_length=50, blank=True, null=True)
    bio = models.TextField(blank=True, null=True)
    interests = models.CharField(max_length=255, blank=True, null=True)
    goals = models.CharField(max_length=255, blank=True, null=True)
    skills = models.CharField(max_length=255, blank=True, null=True)
    experience_years = models.IntegerField(default=0, blank=True)
    linkedin = models.URLField(max_length=500, blank=True, null=True)
    expertise = models.CharField(max_length=225, blank=True, null=True)
    website = models.URLField(max_length=500, blank=True, null=True)
    X_account = models.CharField(max_length=100, blank=True, null=True)
    is_available = models.BooleanField(default=True, help_text="Is the mentor currently available for mentorship?")
    address = models.CharField(max_length=255, blank=True, null=True)
    phone_number = models.CharField(max_length=20, blank=True, null=True)
    state = models.CharField(max_length=25, blank=True, null=True)
    country = models.CharField(max_length=50, blank=True, null=True)

    class Meta:
        verbose_name = "Mentor"
        verbose_name_plural = "Mentors"

    def __str__(self):
        return f"{self.user.first_name}'s Profile"




# Mentee Model
class MenteeProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='mentee_profile')
    google_credentials = models.JSONField(null=True, blank=True)
    username = models.CharField(max_length=255, blank=True, null=True)
    passport_image = models.ImageField(upload_to='passport_images/', blank=True, null=True)
    passport_image_url = models.URLField(blank=True, null=True)
    company = models.CharField(max_length=255, blank=True, null=True)
    job_title = models.CharField(max_length=255, blank=True, null=True)
    industry = models.CharField(max_length=50, blank=True, null=True)
    bio = models.TextField(blank=True, null=True)
    interests = models.CharField(max_length=255, blank=True, null=True)
    goals = models.CharField(max_length=255, blank=True, null=True)
    skills = models.CharField(max_length=255, blank=True, null=True)
    experience_years = models.IntegerField(default=0, blank=True)
    linkedin = models.URLField(max_length=500, blank=True, null=True)
    expertise = models.CharField(max_length=225, blank=True, null=True)
    website = models.URLField(max_length=500, blank=True, null=True)
    X_account = models.CharField(max_length=100, blank=True, null=True)
    is_available = models.BooleanField(default=True, help_text="Is the mentee currently available for mentorship?")
    address = models.CharField(max_length=255, blank=True, null=True)
    phone_number = models.CharField(max_length=20, blank=True, null=True)
    state = models.CharField(max_length=25, blank=True, null=True)
    country = models.CharField(max_length=50, blank=True, null=True)

    class Meta:
        verbose_name = "Mentee"
        verbose_name_plural = "Mentees"

    def __str__(self):
        return f"{self.user.first_name}'s Profile"







