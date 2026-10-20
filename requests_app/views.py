
"""Views for citizen registration and service-request management."""

from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render

from .forms import CitizenRegistrationForm, ServiceRequestForm
from .models import ServiceRequest


def home(request):
    """Display public statistics about submitted service requests."""
    total_requests = ServiceRequest.objects.count()
    open_requests = ServiceRequest.objects.exclude(
        status=ServiceRequest.Status.RESOLVED
    ).count()
    resolved_requests = ServiceRequest.objects.filter(
        status=ServiceRequest.Status.RESOLVED
    ).count()

    return render(
        request,
        "requests_app/home.html",
        {
            "total_requests": total_requests,
            "open_requests": open_requests,
            "resolved_requests": resolved_requests,
        },
    )


def register(request):
    """Register a citizen and redirect successful registrations to login."""
    if request.method == "POST":
        form = CitizenRegistrationForm(request.POST)

        if form.is_valid():
            form.save()
            return redirect("login")
    else:
        # Show an empty registration form for a new visitor.
        form = CitizenRegistrationForm()

    return render(
        request,
        "requests_app/register.html",
        {"form": form},
    )


@login_required
def submit_request(request):
    """Allow authenticated citizens to submit service requests."""
    if request.method == "POST":
        # Include uploaded files so the optional image is processed.
        form = ServiceRequestForm(request.POST, request.FILES)

        if form.is_valid():
            # Associate the new request with the logged-in citizen rather
            # than trusting a citizen ID supplied by the submitted form.
            service_request = form.save(commit=False)
            service_request.citizen = request.user
            service_request.save()
            return redirect("home")
    else:
        form = ServiceRequestForm()

    return render(
        request,
        "requests_app/submit_request.html",
        {"form": form},
    )


@login_required
def my_requests(request):
    """Show each authenticated citizen only their own requests."""
    service_requests = ServiceRequest.objects.filter(
        citizen=request.user
    )

    return render(
        request,
        "requests_app/my_requests.html",
        {"service_requests": service_requests},
    )
