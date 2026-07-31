from django.shortcuts import get_object_or_404, render

from .models import Project


def project_context(request, context):

    context.update(
        {
            "projects": {
                "list": Project.objects.all(),
            }
        }
    )

    return context


def project_detail(request, project_id):

    project = get_object_or_404(Project, id=project_id)

    return render(
        request,
        "projects/detail.html",
        {
            "project": project,
        },
    )
