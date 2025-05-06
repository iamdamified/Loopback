from django.db import models
from profiles.models import Profile

        
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


