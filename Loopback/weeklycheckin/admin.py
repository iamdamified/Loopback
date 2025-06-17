from django.contrib import admin
from .models import WeeklyCheckIn, WeeklyCheckInFeedback

# Register your models here.


admin.site.register(WeeklyCheckIn)
admin.site.register(WeeklyCheckInFeedback)
