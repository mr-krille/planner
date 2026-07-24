from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import HttpResponseForbidden
from django.db.models import Sum
from datetime import date, timedelta
from .models import Timesheet, TimeEntry
from projects.models import Project

@login_required
def timesheet_dashboard(request):
    """
    View timesheet dashboard
    """
    if request.user.userprofile.role == 'admin':
        # Admin can view all employee timesheets
        timesheets = Timesheet.objects.all().select_related('employee').order_by('-month')
    else:
        # Employee can only view their own timesheets
        timesheets = Timesheet.objects.filter(employee=request.user).select_related('employee').order_by('-month')

    return render(request, 'timesheets/dashboard.html', {'timesheets': timesheets})

@login_required
def create_timesheet(request):
    """
    Create a new timesheet (admin only or employee for their own timesheet)
    """
    if request.user.userprofile.role == 'admin':
        # Admin can create timesheets for any employee
        # For simplicity in this demo, we'll just focus on the employee creation flow
        pass
    else:
        # Employee can create their own timesheet for current month
        if request.method == 'POST':
            month = request.POST.get('month')
            # In a real application, this would create a new timesheet for the current month

    return render(request, 'timesheets/create_timesheet.html')

@login_required
def view_timesheet(request, timesheet_id):
    """
    View a specific timesheet with entries
    """
    timesheet = get_object_or_404(Timesheet, id=timesheet_id)

    # Check permissions
    if request.user.userprofile.role == 'employee' and timesheet.employee != request.user:
        return HttpResponseForbidden("You don't have permission to view this timesheet.")

    # Get all time entries for this timesheet
    time_entries = TimeEntry.objects.filter(timesheet=timesheet).select_related('project').order_by('date')

    # Calculate total hours
    total_hours = time_entries.aggregate(Sum('hours'))['hours__sum'] or 0

    return render(request, 'timesheets/view_timesheet.html', {
        'timesheet': timesheet,
        'time_entries': time_entries,
        'total_hours': total_hours
    })

@login_required
def create_time_entry(request, timesheet_id):
    """
    Create a new time entry (admin or employee for their own timesheet)
    """
    timesheet = get_object_or_404(Timesheet, id=timesheet_id)

    # Check permissions
    if request.user.userprofile.role == 'employee' and timesheet.employee != request.user:
        return HttpResponseForbidden("You don't have permission to add entries to this timesheet.")

    if request.method == 'POST':
        # Process form to create time entry
        project_id = request.POST.get('project')
        entry_date = request.POST.get('date')
        hours = request.POST.get('hours')
        description = request.POST.get('description')

        # In a real implementation, we would validate and save the entry

        messages.success(request, 'Time entry added successfully.')
        return redirect('view_timesheet', timesheet_id=timesheet.id)

    projects = Project.objects.all() if request.user.userprofile.role == 'admin' else Project.objects.filter(created_by=request.user)

    return render(request, 'timesheets/create_time_entry.html', {
        'timesheet': timesheet,
        'projects': projects
    })

@login_required
def generate_monthly_report(request):
    """
    Generate monthly report (admin view)
    """
    if request.user.userprofile.role != 'admin':
        return HttpResponseForbidden("Only administrators can generate reports.")

    # For demonstration, we're creating a simple report view
    reports = MonthlyReport.objects.all().select_related('employee').order_by('-month')

    return render(request, 'timesheets/monthly_report.html', {'reports': reports})
