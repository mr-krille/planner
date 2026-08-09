from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import Group
from unfold.admin import ModelAdmin
from unfold.forms import AdminPasswordChangeForm, UserChangeForm, UserCreationForm

from .models import User, UserProfile

admin.site.unregister(Group)


# Extend the UserAdmin to show the role field
class UserProfileInline(admin.StackedInline):
    model = UserProfile
    can_delete = False
    verbose_name_plural = "User Profile"


@admin.register(User)
class UserAdmin(BaseUserAdmin, ModelAdmin):
    # Forms loaded from `unfold.forms`
    form = UserChangeForm
    add_form = UserCreationForm
    change_password_form = AdminPasswordChangeForm
    inlines = (UserProfileInline,)
