from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.models import User
from django.http import HttpResponseForbidden
from .models import Project, File
from .forms import ProjectForm, FileUploadForm

@login_required
def project_list(request):
    """
    List all projects the user has access to
    """
    if request.user.userprofile.role == 'admin':
        projects = Project.objects.all()
    else:
        # Employees can only see projects they're assigned to
        projects = Project.objects.filter(assigned_employees=request.user)

    return render(request, 'projects/project_list.html', {'projects': projects})

@login_required
def project_detail(request, project_id):
    """
    View project details and files
    """
    project = get_object_or_404(Project, id=project_id)

    # Check permissions
    if request.user.userprofile.role == 'employee':
        if project.created_by != request.user and request.user not in project.assigned_employees.all():
            return HttpResponseForbidden("You don't have permission to view this project.")

    files = File.objects.filter(project=project)

    return render(request, 'projects/project_detail.html', {
        'project': project,
        'files': files
    })

@login_required
def create_project(request):
    """
    Create a new project (admin only)
    """
    if request.user.userprofile.role != 'admin':
        return HttpResponseForbidden("Only administrators can create projects.")

    if request.method == 'POST':
        form = ProjectForm(request.POST)
        if form.is_valid():
            project = form.save(commit=False)
            project.created_by = request.user
            project.save()
            messages.success(request, 'Project created successfully.')
            return redirect('project_detail', project_id=project.id)
    else:
        form = ProjectForm()

    return render(request, 'projects/create_project.html', {'form': form})

@login_required
def upload_file(request, project_id):
    """
    Upload a file to a project (employees can only upload to assigned projects)
    """
    project = get_object_or_404(Project, id=project_id)

    # Check permissions
    if request.user.userprofile.role == 'employee':
        if project.created_by != request.user and request.user not in project.assigned_employees.all():
            return HttpResponseForbidden("You don't have permission to upload files to this project.")

    if request.method == 'POST':
        form = FileUploadForm(request.POST, request.FILES)
        if form.is_valid():
            file_instance = form.save(commit=False)
            file_instance.project = project
            file_instance.owner = request.user
            file_instance.uploaded_by = request.user
            file_instance.save()
            messages.success(request, 'File uploaded successfully.')
            return redirect('project_detail', project_id=project.id)
    else:
        form = FileUploadForm()

    return render(request, 'projects/upload_file.html', {
        'form': form,
        'project': project
    })

@login_required
def delete_file(request, file_id):
    """
    Delete a file (only owner can delete)
    """
    file_instance = get_object_or_404(File, id=file_id)

    # Check if user is the owner or project creator
    if (file_instance.owner != request.user and
        file_instance.project.created_by != request.user):
        return HttpResponseForbidden("You don't have permission to delete this file.")

    if request.method == 'POST':
        file_instance.delete()
        messages.success(request, 'File deleted successfully.')
        return redirect('project_detail', project_id=file_instance.project.id)

    return render(request, 'projects/delete_file.html', {
        'file': file_instance
    })