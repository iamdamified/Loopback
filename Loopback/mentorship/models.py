from datetime import timedelta
from django.utils import timezone
from profiles.models import MenteeProfile, MentorProfile
from django.contrib.auth import get_user_model
from django.db import models

class MentorshipLoop(models.Model):
    mentor = models.ForeignKey(MentorProfile, on_delete=models.CASCADE)
    mentee = models.ForeignKey(MenteeProfile, on_delete=models.CASCADE)
    start_date = models.DateField(default=timezone.now)
    end_date = models.DateField(default=timezone.now() + timedelta(weeks=4))
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"Loop: {self.mentee.user.first_name} & {self.mentor.user.first_name}"