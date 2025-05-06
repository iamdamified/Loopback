from django.db import models
from profiles.models import Profile

# Create your models here.
# LOOP INFORMATION FOR ORGANISATION
# This is a mentorship loop between a mentor and a mentee.

class MatchRequest(models.Model):
    mentor = models.ForeignKey(Profile, related_name='incoming_requests', on_delete=models.CASCADE)
    mentee = models.ForeignKey(Profile, related_name='outgoing_requests', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    is_approved = models.BooleanField(default=False)
    responded = models.BooleanField(default=False)

    class Meta:
        unique_together = ('mentor', 'mentee')