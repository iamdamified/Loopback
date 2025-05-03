from django.db import models
from django.conf import settings
from mentorship.models import Mentorship
# Create your models here.

class Weeklycheckin(models.Model):
    loop = models.ForeignKey("mentorship.Mentorship", on_delete=models.CASCADE, related_name="checkins")
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    week_id = models.PositiveIntegerField()
    progress = models.TextField(blank=True, null=True)
    challenges = models.TextField(blank=True, null=True)
    feedback = models.TextField(blank=True, null=True)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('loop', 'week_id', 'created_by')

    def __str__(self):
        return f"Check-in for {self.loop} for week {self.week_id} by {self.created_by.username}({self.created_by.role})"


# Create your models here.
