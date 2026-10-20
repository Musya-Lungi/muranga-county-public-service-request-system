
#!/usr/bin/env python
"""
Django command-line entry point for the Murang'a County Public Service
Request System.

This file allows developers and administrators to run Django management
commands such as starting the development server, applying database
migrations, creating administrators, and running automated tests.
"""

import os
import sys


def main():
    """Configure Django and execute the requested management command."""

    # Tell Django which settings module contains the project configuration.
    # setdefault preserves this variable if it has already been configured
    # by the environment, for example by a production hosting platform.
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')

    try:
        # Import Django's command-line dispatcher only when it is needed.
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        # Provide a helpful error if Django cannot be imported, commonly
        # because dependencies are missing or the virtual environment is
        # not activated.
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc

    # Pass the command-line arguments to Django.
    # For example, "python manage.py test" runs the project's test suite.
    execute_from_command_line(sys.argv)


# Run main() only when this file is executed directly, not when imported
# as a module by another Python file.
if __name__ == '__main__':
    main()
