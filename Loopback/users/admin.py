from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User

#

# Register your models here.


class UserAdmin(BaseUserAdmin):
    fieldsets = BaseUserAdmin.fieldsets + (
        (None, {'fields': ('verified', 'role')}),
    )
    list_display = BaseUserAdmin.list_display + ('verified', 'role')

admin.site.register(User, UserAdmin)




