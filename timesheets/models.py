from django.db import models
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from datetime import date

class Timesheet(models.Model):
    """
    Monthly timesheet model to track employee work
    """
    employee = models.ForeignKey(User, on_delete=models.CASCADE, related_name='timesheets')
    month = models.DateField()  # This will represent the month (first day of the month)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.employee.username} - {self.month.strftime('%Y-%m')}"

    class Meta:
        unique_together = ['employee', 'month']

class TimeEntry(models.Model):
    """
    Individual time entry model
    """
    timesheet = models.ForeignKey(Timesheet, on_delete=models.CASCADE, related_name='time_entries')
    project = models.ForeignKey('projects.Project', on_delete=models.CASCADE)
    date = models.DateField()
    hours = models.DecimalField(max_digits=4, decimal_places=2)
    description = models.TextField(blank=True)

    def clean(self):
        # Prevent entering future dates
        if self.date > date.today():
            raise ValidationError("You cannot enter time entries for future dates.")

        # Ensure the date is within the timesheet month
        if self.date.month != self.timesheet.month.month or self.date.year != self.timesheet.month.year:
            raise ValidationError("The date must be within the timesheet month.")

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.employee.username} - {self.date} - {self.hours} hours"

class MonthlyReport(models.Model):
    """
    Monthly aggregated report model
    """
    employee = models.ForeignKey(User, on_delete=models.CASCADE)
    month = models.DateField()
    total_hours = models.DecimalField(max_digits=6, decimal_places=2, default=0)
    project_hours = models.JSONField(default=dict)  # Stores hours per project

    def __str__(self):
        return f"{self.employee.username} - {self.month.strftime('%Y-%m')} Report"