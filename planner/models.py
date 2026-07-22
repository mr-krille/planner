from django.db import models
from django.contrib.auth.models import User
from datetime import date, timedelta

class WeeklyPlan(models.Model):
    """
    Weekly plan model to organize employee assignments
    """
    week_start = models.DateField()
    week_end = models.DateField()
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='created_weekly_plans')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Week of {self.week_start}"

    class Meta:
        ordering = ['-week_start']

class DailyAssignment(models.Model):
    """
    Daily assignment model to track employee work per day
    """
    project = models.ForeignKey('projects.Project', on_delete=models.CASCADE, related_name='daily_assignments')
    employee = models.ForeignKey(User, on_delete=models.CASCADE, related_name='daily_assignments')
    weekly_plan = models.ForeignKey(WeeklyPlan, on_delete=models.CASCADE, related_name='daily_assignments')
    date = models.DateField()
    hours = models.DecimalField(max_digits=4, decimal_places=2)
    description = models.TextField(blank=True)

    def __str__(self):
        return f"{self.employee.username} - {self.project.name} - {self.date}"

    class Meta:
        ordering = ['date']
        unique_together = ['employee', 'date', 'project']