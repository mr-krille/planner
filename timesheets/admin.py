from django.contrib import admin
from unfold.admin import ModelAdmin

from .models import Timesheet, TimeEntry


@admin.register(Timesheet)
class TimesheetAdmin(ModelAdmin):
    pass


@admin.register(TimeEntry)
class TimeEntryAdmin(ModelAdmin):
    pass
