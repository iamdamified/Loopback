from django.db import models
from django.core.exceptions import ValidationError
from mentorship.models import MentorshipLoop
from matchrequest.models import MatchRequest

# To be integrated with Google Calendar API for scheduling and reminders
# and to be used in the frontend for displaying scheduled meetings and checkins
class WeeklyCheckInMeetingSchedule(models.Model):
    loop = models.ForeignKey(MentorshipLoop, on_delete=models.CASCADE)
    week_number = models.PositiveSmallIntegerField()
    weekly_goals = models.TextField(blank=True, null=True)
    scheduled_date = models.DateField()
    start_time = models.TimeField(blank=True, null=True)
    end_time = models.TimeField(blank=True, null=True)
    meetining_link = models.URLField(max_length=200, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


    def __str__(self):
        return f"Meeting for {self.loop} - Week {self.week_number} on {self.scheduled_date.strftime('%Y-%m-%d')} at {self.start_time.strftime('%H:%M')} to {self.end_time.strftime('%H:%M')}"




class WeeklyCheckIn(models.Model):
    STATUS_PENDING = 'pending'
    STATUS_COMPLETED = 'completed'

    STATUS_CHOICES = [
        (STATUS_PENDING, 'Pending'),
        (STATUS_COMPLETED, 'Completed'),
    ]

    loop = models.ForeignKey(MentorshipLoop, on_delete=models.CASCADE)
    week_number = models.PositiveSmallIntegerField()
    mentor_checked_in = models.BooleanField(default=False)
    mentee_checked_in = models.BooleanField(default=False)
    progress = models.TextField(blank=True, null=True)
    challenges = models.TextField(blank=True, null=True)
    feedback = models.TextField(blank=True, null=True)
    checkin_date = models.DateField()
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default=STATUS_PENDING)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('loop', 'week_number')

    def __str__(self):
        return f"Check-in for {self.loop} - Week {self.week_number} on {self.checkin_date.strftime('%Y-%m-%d')}"

    def clean(self):
        if not (1 <= self.week_number <= 4):
            raise ValidationError("Week number must be between 1 and 4.")
        
    def save(self, *args, **kwargs):
        # Auto-update status
        if self.mentor_checked_in and self.mentee_checked_in:
            self.status = self.STATUS_COMPLETED
        else:
            self.status = self.STATUS_PENDING
        super().save(*args, **kwargs)
