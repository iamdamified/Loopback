from django.contrib.auth import get_user_model
from django.db import models
from profiles.models import MenteeProfile, MentorProfile


class MatchRequest(models.Model):
    mentee = models.ForeignKey(MenteeProfile, on_delete=models.CASCADE)
    mentor = models.ForeignKey(MentorProfile, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=10, choices=[
        ('pending', 'Pending'),
        ('accepted', 'Accepted'),
        ('declined', 'Declined'),
    ], default='pending')

    class Meta:
        unique_together = ('mentee', 'mentor')

    def __str__(self):
        return f"{self.mentee.user.first_name} → {self.mentor.user.first_name} [{self.status}]"