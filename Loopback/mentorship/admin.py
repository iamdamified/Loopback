from django.contrib import admin
from .models import MentorshipLoop
# from django_celery_beat.models import PeriodicTasks


# # Optional: allows more advanced scheduling
# admin.site.register(PeriodicTasks)


admin.site.register(MentorshipLoop)

