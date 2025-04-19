from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User, Profile, Mentorship, Goal, Weeklycheckin, LoopFeedback
#

# Register your models here.


class UserAdmin(BaseUserAdmin):
    fieldsets = BaseUserAdmin.fieldsets + (
        (None, {'fields': ('verified', 'role')}),
    )
    list_display = BaseUserAdmin.list_display + ('verified', 'role')

admin.site.register(User, UserAdmin)

admin.site.register(Profile)

admin.site.register(Mentorship)

admin.site.register(Goal)

admin.site.register(Weeklycheckin)

admin.site.register(LoopFeedback)
