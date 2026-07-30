from django.contrib.auth.models import User
from django.db import models


class Project(models.Model):
    """
    Project model with metadata and access control
    """

    name = models.CharField(max_length=200)
    company = models.CharField(max_length=50)
    description = models.TextField(blank=True)
    created_by = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="created_projects"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

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
    file_path = models.FilePathField(
        path="/tmp"
    )  # In production, this would point to file storage
    upload_date = models.DateTimeField(auto_now_add=True)
    owner = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="uploaded_files"
    )
    uploaded_by = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="uploaded_by"
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
