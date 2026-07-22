from django.urls import path
from . import views

urlpatterns = [
    path('projects/', views.project_list, name='project_list'),
    path('projects/<int:project_id>/', views.project_detail, name='project_detail'),
    path('projects/create/', views.create_project, name='create_project'),
    path('projects/<int:project_id>/upload/', views.upload_file, name='upload_file'),
    path('files/<int:file_id>/delete/', views.delete_file, name='delete_file'),
]