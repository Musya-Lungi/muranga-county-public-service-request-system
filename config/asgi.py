
"""
ASGI configuration for the Murang'a County Public Service Request System.

ASGI (Asynchronous Server Gateway Interface) provides an entry point for
servers that support asynchronous Python web applications.

The module-level variable named ``application`` is the callable used by
an ASGI-compatible server to communicate with Django.

Documentation:
https://docs.djangoproject.com/en/6.1/howto/deployment/asgi/
"""

import os

# Import Django's factory for creating the ASGI application callable.
from django.core.asgi import get_asgi_application

# Identify the Django settings module used to configure the project.
# setdefault keeps an existing environment-provided value unchanged.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')

# Initialise Django and expose the ASGI application to the server.
application = get_asgi_application()
