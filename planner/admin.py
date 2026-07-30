from django.contrib import admin
from unfold.admin import ModelAdmin

from .models import Assignment


@admin.register(Assignment)
class AssignmentAdmin(ModelAdmin):
    pass
