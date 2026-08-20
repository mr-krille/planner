# Company Management Platform

A Django platform for managing projects, weekly work assignments, and monthly timesheets for a
German electrical firm. Two operating companies: `JE` = "Jede Elektro" and `EW` = "Elektro Wolff".
Language/locale is German (`de-de`, timezone `Europe/Berlin`); UI text and model labels are in German.

- **Django 6.0.7**, SQLite, run from `manage.py` (settings module `core.settings`).
- **Two roles:** admin (Django superuser) and employee. The role is stored on a per-user profile.
- **Three domains:** Projects, Planner, Timesheets.

## How the front-end works

The **django-unfold admin (`/admin/`) is the UI shell and the hub** of the app. There is no
`base.html` and no custom `static/` directory — all styling is the Tailwind CSS + Alpine.js that
django-unfold ships.

- `core/settings.py` sets `UNFOLD = {"DASHBOARD_CALLBACK": "core.views.dashboard_callback"}`. That
  callback (`core/views.py`) calls `planner.views.planner_context` and `projects.views.project_context`
  to inject planner and projects data into the admin dashboard context.
- `templates/admin/index.html` (a global override of the admin dashboard) `{% include %}`s three
  fragments and hosts an Alpine.js modal that opens admin add/change forms in an `iframe`
  (`?_popup=1`):
  - `projects/task_list.html` — shown to superusers only
  - `planner/calendar.html` — the weekly assignment grid
  - `projects/project_list.html` — project cards
- `X_FRAME_OPTIONS = 'SAMEORIGIN'` is set so those admin popups can load inside the iframe. On save,
  the admin's popup response (`templates/admin/popup_response.html`) signals the parent frame, which
  closes the modal and reloads the dashboard.

The other two admin overrides are `templates/admin/popup_response.html` and
`templates/admin/submit_line.html`.

## Project layout

```
django_project/
├── manage.py
├── requirements.txt          # asgiref, Django 6.0.7, django-unfold 0.101.0, sqlparse
├── db.sqlite3
├── core/                     # project config: settings.py, urls.py, views.py, wsgi/asgi
├── accounts/                 # auth: custom User + UserProfile (role), register/login
├── projects/                 # Project, Task, File
├── planner/                  # Assignment + week-grid calendar (+ templatetags)
├── timesheets/               # Timesheet, TimeEntry
├── pages/                    # trivial home page
├── templates/admin/          # django-unfold admin overrides
├── media/                    # uploaded files (MEDIA_ROOT)
└── venv/
```

The four domain apps (`accounts`, `projects`, `planner`, `timesheets`) have no `__init__.py` and run
as Python namespace packages; `core` and `pages` do have one.

## Configuration (`core/settings.py`)

- `INSTALLED_APPS`: the four domain apps plus `pages`, then `unfold` (+ its `filters`/`forms`/`inlines`
  contribs), then the standard `django.contrib.*` apps.
- `AUTH_USER_MODEL = 'accounts.User'` (custom user model).
- `MEDIA_ROOT = BASE_DIR / 'media'`, `MEDIA_URL = '/media/'`; media is served in DEBUG only (see
  `core/urls.py`). No `STATICFILES_DIRS`/`STATIC_ROOT` — static assets come from unfold.
- `TIME_ZONE = 'Europe/Berlin'`, `LANGUAGE_CODE = 'de-de'`, `USE_TZ = True`.
- `X_FRAME_OPTIONS = 'SAMEORIGIN'` (enables the unfold iframe popups).

## URL routing (`core/urls.py`)

Only three things are mounted at the root:

```python
path("admin/", admin.site.urls)
path("", include("projects.urls"))
path("", include("pages.urls"))
# + static(settings.MEDIA_URL, ...) when DEBUG
```

`accounts` and `timesheets` each have a `urls` module that is **not** included in the root urlconf,
and `planner` has no `urls` module at all (it is reachable only through the admin dashboard).

## Accounts (auth)

- Custom `User` extending `AbstractUser` with `USERNAME_FIELD = "email"` and a unique `email`.
- A separate `UserProfile` (`OneToOneField` to the user) holds `role`, with choices
  `admin` / `employee` (default `employee`).
- Two views (in `accounts/views.py`, with standalone login/register templates — no inheritance):
  - `register` — creates the `User` and its `UserProfile` (with the chosen role).
  - `login_view` — authenticates and then `redirect('dashboard')`.

## Projects app

Models (`projects/models.py`):

- **`Project`** — `name`, `company` (choices `JE`/`EW`, default `EW`), `color`, `description`,
  `created_by` (FK user, set to the creating admin), `created_at`/`updated_at`. `shortname()` returns
  `<company>-<year>-0<id>` (a literal `0` prepended to the raw id, e.g. `EW-2026-07` for id 7).
- **`Task`** — a global to-do item (no project FK): `name`, `color`, `description`, `due_date`,
  `is_done` (default False), `created_by`, timestamps.
- **`File`** — `name`, `project` (FK), `file` (`FileField`, no `upload_to` → stored at the media root),
  `upload_date`, `owner` (FK user).

Color is one of eight choices (hex value → German color name). All create/edit/delete — including file
upload/download/delete — happens through the django-unfold admin (`ProjectAdmin`, `TaskAdmin`,
`FileAdmin` in `projects/admin.py`), which uses custom color/company radio widgets and sets
`created_by` to the current user. Two read-only detail views also exist: `project_detail` and
`task_detail` (routed in `projects/urls.py`), rendered in unfold-style detail templates.

## Planner app

A single model:

- **`Assignment`** — `employee` (FK user), `project` (FK `projects.Project`), `start_date` and
  `end_date` (DateFields — an assignment is a date range, there are no per-day rows and no hours), and
  `description` (label "Notizen").

There is no `urls.py`; the planner is used entirely through the admin dashboard:

- `planner/views.py` exposes `planner_context(request, context)`, which computes today, the
  start/end of the week, the working-day columns, all assignments, and the "free" (unassigned)
  employees, and stores them under `context["planner"]`.
- `templates/planner/calendar.html` renders a two-week weekday grid, grouping assignments by employee.
  `planner/templatetags/planner_tags.py` provides the `grid_span` / `grid_start` filters that map an
  assignment's date range onto the grid columns.
- Assigning / adding / prefilling opens the admin `Assignment` add or change form as a `?_popup=1`
  iframe; for the "+" prefill buttons, GET params (`employee`, `start_date`) prefill the form.

## Timesheets app

Models (`timesheets/models.py`):

- **`Timesheet`** — `employee` (FK user), `month` (a `DateField` holding the first day of the month),
  timestamps. Unique per `(employee, month)`.
- **`TimeEntry`** — `timesheet` (FK), `project` (FK, `SET_NULL`, nullable), `date`, `hours`
  (Decimal 4,2), `description`. `clean()` rejects future dates and dates that fall outside the
  timesheet's month; `save()` runs `full_clean()`.

Views (`timesheets/views.py`, all `@login_required`; permission decided from
`request.user.userprofile.role`):

- `timesheet_dashboard` — lists timesheets (admin: all; employee: own only).
- `view_timesheet` — shows a timesheet's entries with a total-hours aggregate (admin: any;
  employee: own only, else 403).
- `create_time_entry` — form to add a time entry to a timesheet (admin: any; employee: own only).
- `create_timesheet` — timesheet creation view.
- `generate_monthly_report` — monthly report view (admin only).

These routes are defined in `timesheets/urls.py` but that module is not included in the root urlconf.
`Timesheet` and `TimeEntry` are both registered with plain django-unfold `ModelAdmin`.

## Pages app

A minimal home page (`home_view` in `pages/views.py` → `pages/templates/pages/home.html`, a standalone
"Hello World" document) served at `""`.

## Templates & styling

There is no base template. Three patterns are in use:

1. **Dashboard fragments** — `project_list.html`, `task_list.html`, `calendar.html` contain only a
   `{% block content %}` body (no `{% extends %}`) and are `{% include %}`d by `admin/index.html`.
2. **Full modal pages** — `project_detail.html` and `task_detail.html` extend
   `unfold/layouts/skeleton.html` so they render with full unfold chrome inside the iframe.
3. **Standalone documents** — the pages home, and the accounts login/register pages, are self-contained
   HTML documents with no inheritance.

Styling is done with unfold's bundled Tailwind utilities + Alpine.js directives; a few templates add
small inline `<style>` blocks. `planner_tags` supplies the calendar grid filters.

## Patterns in use (how the pieces fit)

- **New admin-managed object:** register it with `unfold.admin.ModelAdmin` in the app's `admin.py` —
  it then appears in the admin sidebar with add/change/delete popups.
- **New dashboard section:** add a fragment template, `{% include %}` it in `templates/admin/index.html`
  (gating on `user.is_superuser` where needed), and feed it data by adding a call in
  `core/views.py:dashboard_callback`.
- **New standalone page:** add a URL in the app's `urls.py`, `include()` it in `core/urls.py`, and have
  the template extend `unfold/layouts/skeleton.html` (for a full admin-style page) or stand alone.
