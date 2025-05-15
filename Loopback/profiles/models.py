from django.db import models
# from users.models import User
from django.contrib.auth import get_user_model

User = get_user_model()



INDUSTRY_CHOICES = [
    ('tech', 'Technology'),
    ('finance', 'Finance'),
    ('healthcare', 'Healthcare'),
    ('education', 'Education'),
    ('marketing', 'Marketing'),
    ('legal', 'Legal'),
    ('manufacturing', 'Manufacturing'),
    ('retail', 'Retail'),
    ('construction', 'Construction'),
    ('other', 'Other'),
]

# Create your models here.
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    bio = models.TextField(blank=True, null=True)
    interests = models.ManyToManyField('Interest')
    goals = models.CharField(max_length=255, blank=True, null=True)
    skills = models.ManyToManyField('Skill')
    experience = models.IntegerField(default=0)
    company = models.CharField(max_length=255, blank=True, null=True)
    linkedin = models.URLField(max_length=500, blank=True, null=True)
    website = models.URLField(max_length=500, blank=True, null=True)
    job_title = models.CharField(max_length=255, blank=True, null=True)
    industry = models.CharField(max_length=50, choices=INDUSTRY_CHOICES, blank=True, null=True)
    passport_image = models.ImageField(upload_to='passport_images/', blank=True, null=True)

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