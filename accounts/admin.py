from django.contrib import admin
from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin
from .models import UserProfile

# Extend the UserAdmin to show the role field
class UserProfileInline(admin.StackedInline):
    model = UserProfile
    can_delete = False
    verbose_name_plural = "User Profiles"

class CustomUserAdmin(UserAdmin):
    inlines = (UserProfileInline,)

# Unregister the default UserAdmin and register the new one
admin.site.unregister(User)
admin.site.register(User, CustomUserAdmin)