from planner.views import planner_context
from projects.views import project_context


def dashboard_callback(request, context):
    planner_context(request, context)
    project_context(request, context)
    return context
