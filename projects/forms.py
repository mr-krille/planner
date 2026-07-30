from django import forms

from .models import File, Project


class ProjectForm(forms.ModelForm):
    class Meta:
        model = Project
        fields = ["name", "description"]


class FileUploadForm(forms.ModelForm):
    class Meta:
        model = File
        fields = ["name", "file_path"]
