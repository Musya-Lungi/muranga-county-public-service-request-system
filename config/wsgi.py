
"""
WSGI configuration for the Murang'a County Public Service Request System.

WSGI (Web Server Gateway Interface) allows compatible web servers to
communicate with the Django application.

The module-level variable named ``application`` is the callable that
the WSGI server uses to handle incoming HTTP requests.

Documentation:
https://docs.djangoproject.com/en/6.1/howto/deployment/wsgi/
"""

import os

# Import Django's factory for creating the WSGI application callable.
from django.core.wsgi import get_wsgi_application

# Identify the Django settings module.
# setdefault preserves a settings module already provided by the environment.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')

# Initialise Django and expose the application callable for the WSGI server.
application = get_wsgi_application()
