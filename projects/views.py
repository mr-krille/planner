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
