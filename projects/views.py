from django.shortcuts import get_object_or_404, render

from .models import Project, Task


def project_context(request, context):

    context.update(
        {
            "projects": {
                "list": Project.objects.all(),
                "tasks": Task.objects.filter(is_done=False),
            }
        }
    )

    return context


def project_detail(request, project_id):

    project = get_object_or_404(Project, id=project_id)

    return render(
        request,
        "projects/project_detail.html",
        {
            "project": project,
        },
    )


def task_detail(request, task_id):

    task = get_object_or_404(Task, id=task_id)

    return render(
        request,
        "projects/task_detail.html",
        {
            "task": task,
        },
    )
