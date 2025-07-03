
from django.utils import timezone
from profiles.models import MenteeProfile, MentorProfile
from django.contrib.auth import get_user_model
from django.db import models

def default_start_date():
    return timezone.now().date()

class MentorshipLoop(models.Model):
    mentor = models.ForeignKey(MentorProfile, on_delete=models.CASCADE)
    mentee = models.ForeignKey(MenteeProfile, on_delete=models.CASCADE)
    purpose = models.CharField(max_length=255, blank=True, null=True)
    start_date = models.DateField(default=default_start_date)
    end_date = models.DateField(blank=True, null=True)
    is_active = models.BooleanField(default=True)
    status = models.CharField(max_length=10, choices=[
        ('pending', 'Pending'),
        ('ongoing', 'Ongoing'),
        ('completed', 'Completed')
    ], default='pending')

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Loop: {self.mentee.user.first_name} & {self.mentor.user.first_name} [{self.status}]"
    