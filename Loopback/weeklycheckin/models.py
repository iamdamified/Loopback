from django.db import models
from django.core.exceptions import ValidationError
from mentorship.models import MentorshipLoop


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
