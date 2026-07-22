from django.urls import path
from . import views

urlpatterns = [
    path('planner/', views.planner_dashboard, name='planner_dashboard'),
    path('planner/<int:plan_id>/', views.view_weekly_plan, name='view_weekly_plan'),
    path('planner/create/', views.create_weekly_plan, name='create_weekly_plan'),
    path('schedule/', views.employee_schedule, name='employee_schedule'),
]