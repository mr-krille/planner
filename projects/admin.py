from django.contrib import admin
from unfold.admin import ModelAdmin

from .models import Project, File


@admin.register(Project)
class ProjectAdmin(ModelAdmin):
    pass


@admin.register(File)
class FileAdmin(ModelAdmin):
    pass
