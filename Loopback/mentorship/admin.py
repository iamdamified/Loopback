from django.contrib import admin
from .models import Mentorship, Goal, MatchRequest
# Register your models here.


admin.site.register(Mentorship)

admin.site.register(Goal)

admin.site.register(MatchRequest)