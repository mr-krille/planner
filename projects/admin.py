from django.contrib import admin
from django.forms.widgets import RadioSelect
from unfold.admin import ModelAdmin

from .models import COLORS, File, Project, Task


class ColorSelect(RadioSelect):
    template_name = "projects/color_widget.html"


class WithColorWidget:
    def get_form(self, request, obj=None, change=False, **kwargs):
        form = super().get_form(request, obj, change, **kwargs)
        form.base_fields["color"].widget = ColorSelect(choices=COLORS)
        return form


class WithCreatedByCurrentUser:
    # readonly_fields = ["created_by"]

    def save_model(self, request, obj, form, change):
        obj.created_by = request.user
        obj.save()


@admin.register(Project)
class ProjectAdmin(WithColorWidget, WithCreatedByCurrentUser, ModelAdmin):
    pass


@admin.register(Task)
class TaskAdmin(WithColorWidget, WithCreatedByCurrentUser, ModelAdmin):
    pass


@admin.register(File)
class FileAdmin(ModelAdmin):
    pass
