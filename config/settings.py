
"""
Django configuration for the Murang'a County Public Service Request System.

This module defines the project's applications, middleware, database,
templates, authentication, security, and file-storage settings.

For additional configuration options, see:
https://docs.djangoproject.com/en/6.1/topics/settings/
"""

import os
from pathlib import Path


# Resolve the absolute path to the project root directory.
# This allows other settings to reference files and folders reliably,
# regardless of the directory from which Django is started.
BASE_DIR = Path(__file__).resolve().parent.parent


# SECURITY: Read the secret key from the environment when available.
# The fallback key is intended only for local development.
# Production deployments must provide a strong, private DJANGO_SECRET_KEY.
SECRET_KEY = os.environ.get(
    "DJANGO_SECRET_KEY",
    "django-insecure-local-development-only-key-change-me",
)

# Enable detailed debugging information only when explicitly configured.
# Debug mode should be disabled on a publicly accessible production site.
DEBUG = os.environ.get("DJANGO_DEBUG", "True").lower() == "true"

# Read permitted hostnames from the environment.
# The defaults support local development; production must supply its own
# hostname through DJANGO_ALLOWED_HOSTS.
# Splitting on commas permits multiple hosts to be configured.
ALLOWED_HOSTS = [
    host.strip()
    for host in os.environ.get(
        "DJANGO_ALLOWED_HOSTS",
        "127.0.0.1,localhost",
    ).split(",")
    if host.strip()
]


# Register the Django applications used by this project.
INSTALLED_APPS = [
    # Register the project app first so its admin templates can override
    # Django's built-in admin templates where matching paths are provided.
    'requests_app',

    # Django's built-in administration, authentication, database model,
    # session, messaging, and static-file applications.
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
]


# Middleware processes incoming requests and outgoing responses.
# These components provide security protections, sessions, URL handling,
# CSRF protection, authentication, messages, and clickjacking protection.
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

# Identify the main URL configuration module for the project.
ROOT_URLCONF = 'config.urls'


# Configure Django's template engine and template discovery.
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',

        # No additional project-level template directories are configured.
        'DIRS': [],

        # Allow Django to discover templates inside installed applications.
        'APP_DIRS': True,

        'OPTIONS': {
            'context_processors': [
                # Makes the current request available to templates.
                'django.template.context_processors.request',

                # Exposes the authenticated user and permission context.
                'django.contrib.auth.context_processors.auth',

                # Makes queued Django messages available in templates.
                'django.contrib.messages.context_processors.messages',

                # Adds service-request totals by status to the admin dashboard.
                'requests_app.context_processors.admin_dashboard_stats',
            ],
        },
    },
]

# Specify the WSGI application used by compatible web servers.
WSGI_APPLICATION = 'config.wsgi.application'


# DATABASE CONFIGURATION
# Use SQLite for this project. The database file is stored in the project
# root directory, which makes local development and assessment setup simple.
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}


# PASSWORD VALIDATION
# Apply Django's built-in checks when users create or change passwords.
AUTH_PASSWORD_VALIDATORS = [
    {
        # Reject passwords that closely resemble the user's personal details.
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        # Require passwords to meet Django's configured minimum length.
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        # Reject commonly used or easily guessed passwords.
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        # Reject passwords made entirely of numeric characters.
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# INTERNATIONALIZATION AND TIME
# Set the default language and configure date/time handling.
LANGUAGE_CODE = 'en-us'

# Store and interpret application datetimes using UTC.
TIME_ZONE = 'UTC'

# Enable Django's internationalization support.
USE_I18N = True

# Use timezone-aware datetimes for safer date and time handling.
USE_TZ = True


# STATIC FILES
# Define the URL prefix used to reference CSS, JavaScript, and other
# static assets. Production hosting may require a separate collection step.
STATIC_URL = 'static/'


# EMAIL CONFIGURATION
# Use Django's console email backend. During development, generated email
# messages are written to the console instead of being sent externally.
# Configure a real email backend separately if production email is required.
MAILERS = {
    'default': {
        'BACKEND': 'django.core.mail.backends.console.EmailBackend',
    },
}


# AUTHENTICATION REDIRECTS
# Specify the login URL and the destination after successful login.
LOGIN_URL = "/accounts/login/"
LOGIN_REDIRECT_URL = "/"


# USER-UPLOADED MEDIA
# Define the URL prefix and filesystem directory for uploaded files,
# including optional images attached to service requests.
MEDIA_URL = "/media/"
MEDIA_ROOT = BASE_DIR / "media"
