from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings

# Create your models here.

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
    interests = models.CharField(max_length=255, blank=True, null=True)
    goals = models.CharField(max_length=255, blank=True, null=True)
    skills = models.CharField(max_length=255, blank=True, null=True)
    experience = models.IntegerField(default=0)

    def __str__(self):
        return f"{self.user.username}'s Profile"



class Mentorship(models.Model):
    STATUS_CHOICES = (
        ('waiting', 'Waiting'),
        ('ongoing', 'Ongoing'),
        ('completed', 'Completed'),
    )

    mentor = models.ForeignKey(settings.AUTH_USER_MODEL, related_name= 'mentor', on_delete=models.CASCADE)
    mentee = models.ForeignKey(settings.AUTH_USER_MODEL, related_name= 'mentee', on_delete=models.CASCADE)
    start_date = models.DateField(auto_created=True)
    end_date = models.DateField(auto_created=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='waiting')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.mentor.username + ' - ' + self.mentee.username + ' - ' + self.status
    


class Goal(models.Model):
    loop = models.ForeignKey(Mentorship, on_delete=models.CASCADE, related_name='goals')
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='created_goals')
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True, null=True)
    completed = models.BooleanField(default=False)

    def __str__(self):
        return self.title + ' - ' + 'Loop ID:' + self.loop.id
    

