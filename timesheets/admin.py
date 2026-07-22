from django.contrib import admin
from .models import Timesheet, TimeEntry, MonthlyReport

admin.site.register(Timesheet)
admin.site.register(TimeEntry)
admin.site.register(MonthlyReport)