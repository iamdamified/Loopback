from django.db import models
from django.conf import settings
from mentorship.models import Mentorship
# Create your models here.

# Success Measurement for Goal achievement
class LoopFeedback(models.Model):
    loop = models.ForeignKey("mentorship.Mentorship", on_delete=models.CASCADE, related_name="feedbacks")
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    rate = models.IntegerField(choices=[(i, str(i)) for i in range(1, 6)])  # 1–5 stars
    successful = models.BooleanField()
    comment = models.TextField(blank=True, null=True)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('loop', 'created_by')

    def __str__(self):
        return f"Feedback from {self.created_by.username} for Loop #{self.loop.id}"