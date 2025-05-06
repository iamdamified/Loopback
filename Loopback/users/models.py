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
    




