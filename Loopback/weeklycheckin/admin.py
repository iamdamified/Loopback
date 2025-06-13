from django.contrib import admin
from .models import WeeklyCheckIn, WeeklyCheckInMeetingSchedule

# Register your models here.


admin.site.register(WeeklyCheckIn)
admin.site.register(WeeklyCheckInMeetingSchedule)
