from django.urls import path
from . import views

urlpatterns = [
    path('timesheets/', views.timesheet_dashboard, name='timesheet_dashboard'),
    path('timesheets/<int:timesheet_id>/', views.view_timesheet, name='view_timesheet'),
    path('timesheets/<int:timesheet_id>/entry/', views.create_time_entry, name='create_time_entry'),
    path('reports/', views.generate_monthly_report, name='generate_monthly_report'),
]