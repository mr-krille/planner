from datetime import datetime, timedelta, timezone

from django.contrib.auth import get_user_model

from .models import Assignment


def planner_context(request, context):
    today = datetime.now(tz=timezone(timedelta(hours=12))).date()
    weekday = today.weekday()  # int 0-6
    start_of_week = today - timedelta(days=weekday)
    end_of_week = start_of_week + timedelta(days=6)

    work_days = []
    current_date = start_of_week
    while len(work_days) < 10:
        if current_date.weekday() < 5:  # 0-4 is Mon-Fri
            work_days.append(current_date)
        current_date += timedelta(days=1)

    assignments = Assignment.objects.all().order_by("employee")
    assigned_users = {
        e["employee__username"] for e in assignments.values("employee__username")
    }

    context.update(
        {
            "planner": {
                "today": today,
                "start_of_week": start_of_week,
                "end_of_week": end_of_week,
                "work_days": work_days,
                "assignments": assignments,
                "free_employees": get_user_model().objects
                    .exclude(username__in=assigned_users)
                    .exclude(is_superuser=True),
            }
        }
    )

    return context
