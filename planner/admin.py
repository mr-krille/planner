from django.contrib import admin
from unfold.admin import ModelAdmin

from .models import Assignment


@admin.register(Assignment)
class AssignmentAdmin(ModelAdmin):
    list_display = ["project", "employee", "start_date", "end_date"]
