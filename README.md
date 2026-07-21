# Django SSR Project

A simple Django project demonstrating server-side rendering.

## Setup Instructions

1. **Create and activate virtual environment**:
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```

2. **Install dependencies**:
   ```bash
   pip install django
   ```

3. **Run migrations**:
   ```bash
   python manage.py migrate
   ```

4. **Start the development server**:
   ```bash
   python manage.py runserver
   ```

5. **Visit the app**: Open [http://127.0.0.1:8000](http://127.0.0.1:8000) in your browser.

## Project Structure
- `core/`: Main project configuration and settings.
- `pages/`: App containing views, URLs, and templates for the frontend pages.
- `venv/`: Python virtual environment (gitignored).

## Verification
The home page should display "Hello World from Django SSR!" rendered directly by the server.
