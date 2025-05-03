from django.db import models
from django.contrib.auth.models import AbstractUser


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
    



# Backend Interests and Skills Definition
class Interest(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Skill(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

