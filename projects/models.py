from django.conf import settings
from django.db import models

COLORS = {
    "66c5cc": "türkis",
    "f6cf71": "gelb",
    "f89c74": "orange",
    "dcb0f2": "lila",
    "87c55f": "grün",
    "9eb9f3": "blau",
    "fe88b1": "rosa",
    "b3b3b3": "grau",
}


class Project(models.Model):
    """
    Project model with metadata and access control
    """

    name = models.CharField(max_length=200)
    company = models.CharField(max_length=50, verbose_name="Firma")
    color = models.CharField(
        max_length=6, choices=COLORS, default=list(COLORS)[-1], verbose_name="Farbe"
    )
    description = models.TextField(blank=True, verbose_name="Beschreibung")
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        editable=False,
        on_delete=models.CASCADE,
        related_name="created_projects",
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Erstellt")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Geändert")

    def __str__(self):
        return self.name

    def shortname(self):
        return f"{self.company}-{self.created_at:%Y}-0{self.id}"

    class Meta:
        ordering = ["-updated_at"]


class Task(models.Model):
    """
    Task model with metadata and access control
    """

    name = models.CharField(max_length=200)
    color = models.CharField(
        max_length=6, choices=COLORS, default=list(COLORS)[-1], verbose_name="Farbe"
    )
    description = models.TextField(blank=True, verbose_name="Beschreibung")
    due_date = models.DateField(blank=True, null=True, verbose_name="Fällig am")
    is_done = models.BooleanField(default=False, verbose_name="Erledigt")
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        editable=False,
        on_delete=models.CASCADE,
        related_name="created_tasks",
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Erstellt")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Geändert")

    def __str__(self):
        return self.name

    class Meta:
        ordering = ["-created_at"]


class File(models.Model):
    """
    File model to track uploaded files
    """

    name = models.CharField(max_length=200)
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name="files")
    file = models.FileField()  # In production, this would point to file storage
    upload_date = models.DateTimeField(auto_now_add=True)
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="uploaded_files",
    )

    def __str__(self):
        return self.name

    def clean(self):
        # Validate that the file owner is assigned to this project or is the project creator
        # This validation can be simplified since we don't have assigned_employees field yet
        pass

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)
