from django.contrib import admin
from .models import Timesheet, TimeEntry

admin.site.register(Timesheet)
admin.site.register(TimeEntry)
