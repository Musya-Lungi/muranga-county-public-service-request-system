
"""
Main URL configuration for the Murang'a County Public Service Request System.

This module connects incoming HTTP requests to Django's administration site,
authentication views, and the service-request application.
"""

# Import Django's helper for serving uploaded media during development.
from django.conf.urls.static import static

# Import Django's built-in administration interface.
from django.contrib import admin

# Import Django's authentication views for login and logout functionality.
from django.contrib.auth import views as auth_views

# Import the project URL-routing functions.
from django.urls import include, path

# Import the project's settings to check whether debug mode is enabled.
from django.conf import settings


# Define the URL patterns available throughout the project.
urlpatterns = [
    # Route /admin/ to Django's administrative interface.
    path("admin/", admin.site.urls),

    # Display the custom login template and name the route "login"
    # so views and templates can reference it by name.
    path(
        "accounts/login/",
        auth_views.LoginView.as_view(
            template_name="requests_app/login.html"
        ),
        name="login",
    ),

    # Log the user out and redirect them to the home page.
    path(
        "accounts/logout/",
        auth_views.LogoutView.as_view(next_page="/"),
        name="logout",
    ),

    # Delegate the remaining application URLs to requests_app.urls.
    # This keeps the project's main routing file concise and organised.
    path("", include("requests_app.urls")),
]


# Serve user-uploaded media files directly through Django only when
# DEBUG is enabled. Production should serve media through its hosting
# configuration or a dedicated media-storage service.
if settings.DEBUG:
    urlpatterns += static(
        settings.MEDIA_URL,
        document_root=settings.MEDIA_ROOT,
    )
