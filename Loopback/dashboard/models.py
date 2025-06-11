# from django.db import models

# # Create your models here.
# from django.db import models
# from django.conf import settings

# class ProgressHistory(models.Model):
#     EVENT_TYPE_CHOICES = [
#         ('goal', 'Goal Set/Updated'),
#         ('meeting', 'Meeting'),
#         ('checkin', 'Check-in'),
#         ('milestone', 'Milestone'),
#         ('feedback', 'Feedback'),
#         ('note', 'Note'),
#         # Add more event types as needed
#     ]

#     mentorship_loop = models.ForeignKey('MentorshipLoop', on_delete=models.CASCADE, related_name='progress_history')
#     user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True, help_text="Who created this event (mentor/mentee/system)?")
#     event_type = models.CharField(max_length=20, choices=EVENT_TYPE_CHOICES)
#     event_date = models.DateTimeField(auto_now_add=True)
#     title = models.CharField(max_length=255, blank=True, null=True)
#     description = models.TextField(blank=True, null=True)
#     extra_data = models.JSONField(blank=True, null=True, help_text="Optional additional info (e.g. week, links, etc)")

#     class Meta:
#         ordering = ['event_date']
#         verbose_name_plural = "Progress History"

#     def __str__(self):
#         return f"{self.mentorship_loop} - {self.get_event_type_display()} on {self.event_date.strftime('%Y-%m-%d')}"