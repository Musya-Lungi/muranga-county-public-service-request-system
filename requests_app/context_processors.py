
"""Provide service-request statistics to the custom admin dashboard."""

from .models import ServiceRequest


def admin_dashboard_stats(request):
    """Return request counts for admin pages only."""

    # Avoid unnecessary database queries on public-facing pages.
    if not request.path.startswith("/admin/"):
        return {}

    requests = ServiceRequest.objects.all()

    # Supply separate counts for the dashboard's summary indicators.
    return {
        "dashboard_total": requests.count(),
        "dashboard_pending": requests.filter(
            status=ServiceRequest.Status.PENDING
        ).count(),
        "dashboard_in_progress": requests.filter(
            status=ServiceRequest.Status.IN_PROGRESS
        ).count(),
        "dashboard_resolved": requests.filter(
            status=ServiceRequest.Status.RESOLVED
        ).count(),
    }
