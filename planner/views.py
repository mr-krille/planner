from datetime import date, datetime, timezone, timedelta

from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import HttpResponseForbidden
from django.db.models import Q

from .models import Assignment


def dashboard_callback(request, context):
    today = datetime.now(tz=timezone(timedelta(hours=12))).date()
    weekday = today.weekday() # int 0-6
    start_of_week = today - timedelta(days=weekday)
    end_of_week = start_of_week + timedelta(days=6)

    work_days = []
    current_date = start_of_week
    while len(work_days) < 10:
        if current_date.weekday() < 5: # 0-4 is Mon-Fri
            work_days.append(current_date)
        current_date += timedelta(days=1)


    context.update({
        'planner': {
            'today': today,
            'start_of_week': start_of_week,
            'end_of_week': end_of_week,
            'work_days': work_days,
            'assignments': Assignment.objects.all(),
        }
    })

    return context


@login_required
def planner_dashboard(request):
    """
    View weekly planner dashboard
    """
    if request.user.userprofile.role == 'admin':
        # Admin can view all weekly plans
        plans = WeeklyPlan.objects.all().order_by('-week_start')
    else:
        # Employees can only see their own assignments
        plans = WeeklyPlan.objects.filter(
            daily_assignments__employee=request.user
        ).distinct().order_by('-week_start')

    return render(request, 'planner/dashboard.html', {'plans': plans})

@login_required
def view_weekly_plan(request, plan_id):
    """
    View a specific weekly plan
    """
    plan = get_object_or_404(WeeklyPlan, id=plan_id)

    # Check permissions
    if request.user.userprofile.role == 'employee':
        if not plan.daily_assignments.filter(employee=request.user).exists():
            return HttpResponseForbidden("You don't have permission to view this plan.")

    # Get all daily assignments for this plan
    assignments = DailyAssignment.objects.filter(weekly_plan=plan).select_related('employee', 'project')

    return render(request, 'planner/view_plan.html', {
        'plan': plan,
        'assignments': assignments
    })

@login_required
def create_weekly_plan(request):
    """
    Create a new weekly plan (admin only)
    """
    if request.user.userprofile.role != 'admin':
        return HttpResponseForbidden("Only administrators can create weekly plans.")

    if request.method == 'POST':
        # In a real implementation, we'd process the form to create assignments
        week_start = request.POST.get('week_start')
        week_end = request.POST.get('week_end')

        # For demonstration, we're creating a basic plan structure
        plan = WeeklyPlan.objects.create(
            week_start=week_start,
            week_end=week_end,
            created_by=request.user
        )

        messages.success(request, 'Weekly plan created successfully.')
        return redirect('view_weekly_plan', plan_id=plan.id)

    return render(request, 'planner/create_plan.html')

@login_required
def employee_schedule(request):
    """
    View employee's personal schedule for current week
    """
    # Get current week's assignments for the employee
    start_of_week = date.today() - timedelta(days=date.today().weekday())
    end_of_week = start_of_week + timedelta(days=6)

    assignments = DailyAssignment.objects.filter(
        employee=request.user,
        date__gte=start_of_week,
        date__lte=end_of_week
    ).select_related('project').order_by('date')

    return render(request, 'planner/employee_schedule.html', {
        'assignments': assignments,
        'week_start': start_of_week,
        'week_end': end_of_week
    })
