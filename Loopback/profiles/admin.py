from django.contrib import admin
from .models import MentorProfile, MenteeProfile
# from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
# Register your models here.



admin.site.register(MentorProfile)

admin.site.register(MenteeProfile)

# @admin.register(MentorProfile)
# class MentorProfileAdmin(admin.ModelAdmin):
#     list_display = ['get_email', 'user']

#     def get_email(self, obj):
#         return obj.user.email
#     get_email.short_description = 'Email'

# @admin.register(MenteeProfile)
# class MenteeProfileAdmin(admin.ModelAdmin):
#     list_display = ['get_email', 'user']

#     def get_email(self, obj):
#         return obj.user.email
#     get_email.short_description = 'Email'







