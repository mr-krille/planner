from django.contrib import admin
from unfold.admin import ModelAdmin

from .models import File, Project, Task


@admin.register(Project)
class ProjectAdmin(ModelAdmin):
    pass


@admin.register(File)
class FileAdmin(ModelAdmin):
    pass


@admin.register(Task)
class TaskAdmin(ModelAdmin):
    pass
