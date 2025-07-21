from django.db import models
from django.core.exceptions import ValidationError
from mentorship.models import MentorshipLoop
from matchrequest.models import MatchRequest
from django.utils import timezone
import datetime


# To be integrated with Google Calendar API for scheduling and reminders
# and to be used in the frontend for displaying scheduled meetings and checkins
class WeeklyCheckIn(models.Model):
    STATUS_PENDING = 'pending'
    STATUS_COMPLETED = 'completed'

    STATUS_CHOICES = [
        (STATUS_PENDING, 'Pending'),
        (STATUS_COMPLETED, 'Completed'),
    ]
    loop = models.ForeignKey(MentorshipLoop, on_delete=models.CASCADE, blank=True, null=True)
    match = models.ForeignKey(MatchRequest, on_delete=models.CASCADE, related_name='checkins', blank=True, null=True) #handles meeting before loop start
    google_event_id = models.CharField(max_length=128, blank=True, null=True, unique=True)
    week_number = models.PositiveSmallIntegerField(blank=True, null=True)
    weekly_goals = models.TextField(blank=True, null=True) # For meeting would be meeting purpose or empty
    scheduled_date = models.DateField(blank=True, null=True)
    start_time = models.TimeField(blank=True, null=True)
    end_time = models.TimeField(blank=True, null=True)
    meetining_link = models.URLField(max_length=200, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default=STATUS_PENDING)
    checkin_created = models.BooleanField(default=False)

    @property
    def is_checkin_created(self):
        return self.google_event_id is not None and self.scheduled_date is not None

    @property
    def is_completed(self):
        """
        Dynamically determines if the check-in has passed its scheduled end time.
        Does NOT change the database.
        """
        if self.scheduled_date and self.end_time:
            end_datetime = datetime.datetime.combine(self.scheduled_date, self.end_time)
            if timezone.is_naive(end_datetime):
                end_datetime = timezone.make_aware(end_datetime)
            return timezone.now() > end_datetime
        return False



    # def __str__(self):
    #     return f"Meeting for {self.loop} - Week {self.week_number} on {self.scheduled_date.strftime('%Y-%m-%d')} at {self.start_time.strftime('%H:%M')} to {self.end_time.strftime('%H:%M')}"

    def __str__(self):
        date_str = self.scheduled_date.strftime('%Y-%m-%d') if self.scheduled_date else "No date"
        start_str = self.start_time.strftime('%H:%M') if self.start_time else "No start"
        end_str = self.end_time.strftime('%H:%M') if self.end_time else "No end"
        week_str = f"Week {self.week_number}" if self.week_number is not None else "No week"
        return f"Check-in for {week_str} on {date_str} at {start_str} to {end_str}"
    
    def clean(self):
        if not (0 <= self.week_number <= 4):
            raise ValidationError("Week number must be between 0 and 4.")
        
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)




# In case we do not need to create separate feedback for Weekly Check-ins, we can takeout STATUS
# and add it to the WeeklyCheckinMeetingSchedule model above for progress tracking, then delete this model.
# in this case, loop field must be optional, ensure not to add unique_together, and adjust clean to 0 to 4 to make space for 0week(first meeting schedule)
class WeeklyCheckInFeedback(models.Model):
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
