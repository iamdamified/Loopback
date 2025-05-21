from django.db import models
from django.conf import settings
from mentorship.models import MentorshipLoop
# Create your models here.


class WeeklyCheckIn(models.Model):
    loop = models.ForeignKey(MentorshipLoop, on_delete=models.CASCADE)
    week_number = models.PositiveSmallIntegerField()
    mentor_checked_in = models.BooleanField(default=False)
    mentee_checked_in = models.BooleanField(default=False)
    progress = models.TextField(blank=True, null=True)
    challenges = models.TextField(blank=True, null=True)
    feedback = models.TextField(blank=True, null=True)
    checkin_date = models.DateField(auto_now_add=True)

    class Meta:
        unique_together = ('loop', 'week_number', 'checkin_date')

    def __str__(self):
        return f"Check-in for {self.loop} for week {self.week_number}"
