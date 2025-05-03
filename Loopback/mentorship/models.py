from django.db import models
from users.models import Profile
from django.conf import settings

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



        
class Mentorship(models.Model):
    STATUS_CHOICES = (
        ('waiting', 'Waiting'),
        ('ongoing', 'Ongoing'),
        ('completed', 'Completed'),
    )

    mentor = models.ForeignKey(Profile, related_name= 'mentor_loops', on_delete=models.CASCADE)
    mentee = models.ForeignKey(Profile, related_name= 'mentee_loops', on_delete=models.CASCADE)
    start_date = models.DateField(auto_created=True)
    finish_date = models.DateField(auto_created=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='waiting')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('mentor', 'mentee') # Prevent duplicate loops

    def __str__(self):
        return self.mentor.username + ' - ' + self.mentee.username + ' - ' + self.status



class Goal(models.Model):
    loop = models.ForeignKey(Mentorship, on_delete=models.CASCADE, related_name='goals')
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='created_goals')
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True, null=True)
    completed = models.BooleanField(default=False)

    def __str__(self):
        return self.title + ' - ' + 'Loop ID:' + ' - ' + self.loop.id