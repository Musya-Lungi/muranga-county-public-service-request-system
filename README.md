
# Murang'a County Public Service Request System

A Django-based web application that enables citizens to report
community service issues and track their resolution.

## Features

- Citizen registration, login, and logout
- Submit service requests with category, title, description,
  location, and an optional image
- Track personal requests and their statuses
- Unique reference numbers for service requests
- Request status workflow: Pending, In Progress, Resolved
- Staff request management through Django Admin
- Homepage statistics for open and resolved requests
- Resolution timestamps
- Automated tests for core functionality and access control

## Technology Stack

- Python
- Django
- SQLite for local development
- HTML and CSS

## Local Setup

1. Install Python and create a virtual environment.
2. Activate the virtual environment.
3. Install dependencies:

   `pip install -r requirements.txt`

4. Apply database migrations:

   `python manage.py migrate`

5. Create an administrator account:

   `python manage.py createsuperuser`

6. Start the development server:

   `python manage.py runserver`

7. Open `http://127.0.0.1:8000/` in your browser.

## Administration

Open `http://127.0.0.1:8000/admin/` and sign in with an
administrator account to manage service requests.

## Testing

Run the automated tests with:

`python manage.py test requests_app`

The current test suite covers registration, login, request
submission, citizen privacy, status handling, and homepage analytics.

## Development Notes

This project currently uses SQLite and Django's development server.
Production deployment requires appropriate production settings,
secure secret management, a production database where appropriate,
and suitable media storage.


