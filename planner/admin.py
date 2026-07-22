from django.contrib import admin
from .models import WeeklyPlan, DailyAssignment

admin.site.register(WeeklyPlan)
admin.site.register(DailyAssignment)