from django.db import models
from django.conf import settings
from mentorship.models import MentorshipLoop
from django.contrib.auth import get_user_model
from users.models import User

# Create your models here.


# class LoopFeedback(models.Model):
#     loop = models.OneToOneField(MentorshipLoop, on_delete=models.CASCADE)
#     mentor_feedback = models.TextField(blank=True)
#     mentee_feedback = models.TextField(blank=True)
#     submitted_at = models.DateTimeField(auto_now_add=True)
#     rate = models.IntegerField(choices=[(i, str(i)) for i in range(1, 6)])  # 1–5 stars
#     successful = models.BooleanField()

#     class Meta:
#         unique_together = ('loop', 'submitted_at')

#     def __str__(self):
#         return f"Feedback for Loop #{self.loop.id}"
    

# User = get_user_model()
class MentorshipFeedback(models.Model):
    loop = models.ForeignKey(MentorshipLoop, on_delete=models.CASCADE, related_name='feedbacks')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    comments = models.TextField()
    submitted_at = models.DateTimeField(auto_now_add=True)
    rate = models.IntegerField(choices=[(i, str(i)) for i in range(1, 6)])  # 1–5 stars
    successful = models.BooleanField()

    class Meta:
        unique_together = ('loop', 'user')  # Prevent multiple submissions

    def __str__(self):
        return f"Feedback from {self.user.email} on loop {self.loop.id}"