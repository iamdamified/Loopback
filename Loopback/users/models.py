from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings
# from api.models import *

# Create your models here.

# USER INFORMATION
class User(AbstractUser):
    ROLE_CHOICES = (
        ('mentor', 'Mentor'),
        ('mentee', 'Mentee')
    )
    role = models.CharField(max_length=10, choices=ROLE_CHOICES)
    verified = models.BooleanField(default=False)

    def __str__(self):
        return self.username + ' - ' + self.role
    


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField(blank=True, null=True)
    interests = models.ManyToManyField('Interest')
    goals = models.CharField(max_length=255, blank=True, null=True)
    skills = models.ManyToManyField('Skill')
    experience = models.IntegerField(default=0)

    def __str__(self):
        return f"{self.user.username}'s Profile"

#HOW TO CREATE PROFILE IN API
# {
#   "username": "mentor",
#   "bio": "I want to guide juniors in Data Science.",
#   "goals": "I want to guide juniors in Data Science.",
#   "experience": "2",
#   "interests": [1, 3],
#   "skills": [2, 4]
# }


class Interest(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Skill(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name




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
    


# Monitoring Tool/Process
class Weeklycheckin(models.Model):
    loop = models.ForeignKey("Mentorship", on_delete=models.CASCADE, related_name="checkins")
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




# Success Measurement for Goal achievement
class LoopFeedback(models.Model):
    loop = models.ForeignKey("Mentorship", on_delete=models.CASCADE, related_name="feedbacks")
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    rate = models.IntegerField(choices=[(i, str(i)) for i in range(1, 6)])  # 1–5 stars
    successful = models.BooleanField()
    comment = models.TextField(blank=True, null=True)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('loop', 'created_by')

    def __str__(self):
        return f"Feedback from {self.created_by.username} for Loop #{self.loop.id}"