# Murang'a County Public Service Request System

A Django-based web application that enables citizens to report community service issues and track their progress towards resolution.

## Features

- Citizen registration, login, and logout
- Submit service requests with category, title, description, location, and an optional image
- View personal service requests and their statuses
- Unique reference numbers for service requests
- Request status workflow: Pending → In Progress → Resolved
- Administrative request management through Django Admin
- Dashboard statistics for total, open, pending, in-progress, and resolved requests
- Automatic resolution timestamps
- Automated tests for core functionality and access control

## Technology Stack

- Python
- Django
- SQLite for local development
- HTML and CSS
- Pillow for image uploads

## Local Setup

1. Install Python.
2. Open a terminal in the project directory.
3. Create and activate a virtual environment:

   ```powershell
   py -3.14 -m venv .venv
   .venv\Scripts\Activate.ps1
   ```

4. Install the project dependencies:

   ```powershell
   python -m pip install Django Pillow
   ```

5. Apply database migrations:

   ```powershell
   python manage.py migrate
   ```

6. Create an administrator account:

   ```powershell
   python manage.py createsuperuser
   ```

7. Start the development server:

   ```powershell
   python manage.py runserver
   ```

8. Open http://127.0.0.1:8000/ in your browser.

## Administration

Open http://127.0.0.1:8000/admin/ and sign in with an administrator account to review requests, update statuses, search records, and filter requests by category or status.

## Testing

Run the automated test suite:

```powershell
python manage.py test
```

The current test suite contains 13 tests covering core application functionality, including registration, authentication, request submission, access control, status handling, and homepage statistics.

## Development and Deployment Notes

The project uses SQLite for local development. Production deployments should use secure environment-based settings, an appropriately configured database, HTTPS, and suitable storage for uploaded media.

Never commit production secret keys, database files containing real user data, or private uploaded files to a public repository.

## Project Purpose

This project demonstrates practical skills in Django development, database modelling, authentication, access control, administrative workflows, automated testing, and user-interface design.
