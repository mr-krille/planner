  Company Management Platform

  1. System Overview

  You want a Django-based managing platform with:
  - Two user types: admin and employees
  - Email-based registration
  - Three core apps: Projects, Planner, Timesheets
  
  2. Platform Architecture

  User Authentication System

  - Django's built-in User model with custom role field
  - Email verification (optional)
  - Role-based permissions (admin/employee)
  - Session management and CSRF protection

  Projects App

  - Projects as virtual folders with associated files
  - Admin can create, edit, delete projects
  - Employees can upload files to assigned projects (per day)
  - Employees can delete their own files only
  - Project access control with validation
  - File metadata tracking (upload date, owner)

  Planner App

  - Weekly planning for all employees
  - Admin assigns projects and hours per day
  - Employees can view their weekly assignments
  - Daily project-hour tracking per employee
  - Planner view with color-coded project assignments

  Timesheets App

  - Monthly time tracking for employees
  - Monthly reviews of hours worked
  - Admin view of aggregated hours by worker/project
  - Time entry validation (cannot enter future dates)
  - Report generation capability

  3. Django Project Structure

  company_platform/
  ├── manage.py
  ├── requirements.txt (Django, etc.)
  ├── .gitignore
  ├── company_platform/
  │   ├── __init__.py
  │   ├── settings.py
  │   ├── urls.py
  │   └── wsgi.py
  ├── accounts/                # Authentication app
  │   ├── __init__.py
  │   ├── models.py
  │   ├── views.py
  │   ├── urls.py
  │   ├── forms.py
  │   └── templates/
  ├── projects/                # Projects app
  │   ├── __init__.py
  │   ├── models.py
  │   ├── views.py
  │   ├── urls.py
  │   ├── forms.py
  │   └── templates/
  ├── planner/                 # Planner app
  │   ├── __init__.py
  │   ├── models.py
  │   ├── views.py
  │   ├── urls.py
  │   ├── forms.py
  │   └── templates/
  ├── timesheets/              # Timesheets app
  │   ├── __init__.py
  │   ├── models.py
  │   ├── views.py
  │   ├── urls.py
  │   ├── forms.py
  │   ├── reports.py
  │   └── templates/
  └── static/                  # CSS, JS, images

  4. Database Design

  Core Tables:

  - User - Django auth user (with role field)
  - Project - Project metadata (name, description, created_by)
  - File - File details (name, path, upload_date, owner)
  - WeeklyPlan - Weekly schedule for employees
  - DailyAssignment - Project assignment per day with hours
  - Timesheet - Monthly time tracking records
  - TimeEntry - Individual time entries with project/date

  5. Core Features Implementation

  User Management:

  - Email registration with role assignment (admin/employee)
  - Django's built-in authentication system
  - User profile management
  - Password reset functionality

  Projects:

  - Admin can create/edit/delete projects
  - Files uploaded to projects are bound to employees
  - File ownership validation
  - Project structure with access control

  Planner:

  - Admin creates weekly plans
  - Assigns projects to employees
  - Specifies hours per project/day
  - Employee view of their weekly assignments
  - Calendar integration for date handling

  Timesheets:

  - Monthly time tracking by employee
  - Administrative view of all timesheets
  - Project-level aggregation reports
  - Validation for time entries (no future dates)
  - Export capability for reports

  6. Security Features

  - Role-based access control (RBAC)
  - File ownership validation for all file operations
  - Project access control at every level
  - CSRF protection for all forms
  - Input validation and sanitization

  7. Development Approach

  1. Phase 1: Setup Django project and authentication
  2. Phase 2: Implement Projects app with file management
  3. Phase 3: Build Planner app for scheduling
  4. Phase 4: Create Timesheets app with reporting
  5. Phase 5: Admin dashboard and integration testing
  6. Phase 6: Security hardening and performance optimization

  8. Requirements Files

  Django==4.2.7
  djangorestframework==3.14.0
  Pillow==10.0.1
  python-decouple==3.8

  9. Deployment Considerations

  - Production-ready settings configuration
  - Database optimization with proper indexing
  - File storage management (local or cloud)
  - Performance monitoring (if needed)
  - Backup strategy for important data

  10. Key Components by App

  Accounts App:

  - Registration view with role selection
  - Login/logout functionality
  - Profile management
  - Password reset

  Projects App:

  - Project CRUD operations (admin only)
  - File upload/download views
  - File permission validation
  - Project access control middleware

  Planner App:

  - Admin view for scheduling weekly plans
  - Employee view of assigned work
  - Calendar input for weekly planning
  - Project-hour assignment forms

  Timesheets App:

  - Monthly report viewer
  - Time entry forms
  - Data validation and error handling
  - Administrative aggregated views
