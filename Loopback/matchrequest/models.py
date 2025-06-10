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
        ('completed', 'Completed')
    ], default='pending')

    class Meta:
        unique_together = ('mentee', 'mentor')

    def __str__(self):
        return f"{self.mentee.user.first_name} → {self.mentor.user.first_name} [{self.status}]"


class MeetingSchedule(models.Model):
    match_request = models.ForeignKey(MatchRequest, on_delete=models.CASCADE, related_name='schedules')
    weekly_goals = models.TextField(blank=True, null=True)
    scheduled_time = models.DateTimeField()
    meetining_link = models.URLField(max_length=200, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Meeting for {self.match_request} at {self.scheduled_time.strftime('%Y-%m-%d %H:%M')}"