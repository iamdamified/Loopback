from django.db import models
from mentorship.models import Mentorship
from django.conf import settings


class Goal(models.Model):
    loop = models.ForeignKey(Mentorship, on_delete=models.CASCADE, related_name='goals')
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='created_goals')
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True, null=True)
    completed = models.BooleanField(default=False)

    def __str__(self):
        return self.title + ' - ' + 'Loop ID:' + ' - ' + self.loop.id

        
# Create your models here.
