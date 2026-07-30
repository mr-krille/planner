from django.db import models
from django.contrib.auth.models import User
from datetime import date, timedelta


class Assignment(models.Model):
    """
    Daily assignment model to track employee work per day
    """
    employee = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Mitarbeiter")
    project = models.ForeignKey('projects.Project', on_delete=models.CASCADE, related_name='task', verbose_name="Projekt")

    start_date = models.DateTimeField(verbose_name="Start")
    end_date = models.DateTimeField(verbose_name="Ende")

    description = models.TextField(blank=True)

    def __str__(self):
        return f"Zuweisung {self.project} - {self.employee} von {self.start_date:%d.%m.} bis {self.end_date:%d.%m.}"

    class Meta:
        ordering = ['-end_date'] # always get latest
        get_latest_by = ["-end_date", "-start_date"]
        verbose_name = "Zuweisung"
        verbose_name_plural = "Zuweisungen"
        # unique_together = ['end_date', 'project', 'employees']
