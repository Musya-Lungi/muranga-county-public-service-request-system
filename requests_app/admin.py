
"""Admin configuration for managing citizen service requests."""

from django.contrib import admin
from django.utils.html import format_html

from .models import ServiceRequest


@admin.register(ServiceRequest)
class ServiceRequestAdmin(admin.ModelAdmin):
    """Customise how administrators review and process requests."""

    # Show key request details and a visual status indicator in the list.
    list_display = (
        "reference_number",
        "title",
        "category",
        "citizen",
        "status_badge",
        "location",
        "created_at",
    )

    # Allow administrators to open a request from its reference or title.
    list_display_links = ("reference_number", "title")

    # Help administrators narrow requests by status, category, and date.
    list_filter = (
        "status",
        "category",
        "created_at",
    )

    # Support searching by request details and the associated citizen.
    search_fields = (
        "reference_number",
        "title",
        "description",
        "location",
        "citizen__username",
        "citizen__first_name",
        "citizen__last_name",
        "citizen__email",
    )

    # Keep generated references and timestamps from being edited directly.
    readonly_fields = (
        "reference_number",
        "created_at",
        "updated_at",
        "resolved_at",
    )

    # Group fields into clear sections to make request management easier.
    fieldsets = (
        (
            "Request Information",
            {
                "fields": (
                    "reference_number",
                    "title",
                    "category",
                    "description",
                    "image",
                )
            },
        ),
        (
            "Citizen and Location",
            {
                "fields": (
                    "citizen",
                    "location",
                )
            },
        ),
        (
            "Processing and Status",
            {
                "fields": (
                    "status",
                    "created_at",
                    "updated_at",
                    "resolved_at",
                )
            },
        ),
    )

    # Improve list ordering, reduce related-user database queries,
    # and keep the administration interface practical to navigate.
    ordering = ("-created_at",)
    list_select_related = ("citizen",)
    list_per_page = 20
    date_hierarchy = "created_at"
    save_on_top = True
    empty_value_display = "—"

    @admin.display(description="Status", ordering="status")
    def status_badge(self, obj):
        """Render the current request status as a coloured label."""

        # Use distinct colours to make each workflow stage easy to identify.
        styles = {
            ServiceRequest.Status.PENDING: (
                "#fff3cd",
                "#805b00",
            ),
            ServiceRequest.Status.IN_PROGRESS: (
                "#dbeafe",
                "#1d4ed8",
            ),
            ServiceRequest.Status.RESOLVED: (
                "#dcfce7",
                "#166534",
            ),
        }

        # Provide a neutral fallback if an unexpected status is encountered.
        background, foreground = styles.get(
            obj.status,
            ("#f3f4f6", "#374151"),
        )

        # format_html safely escapes dynamic text while preserving the
        # intended HTML markup for the status badge.
        return format_html(
            '<span style="display:inline-block;'
            'padding:4px 10px;'
            'border-radius:999px;'
            'font-size:12px;'
            'font-weight:600;'
            'white-space:nowrap;'
            'background-color:{};color:{};">{}</span>',
            background,
            foreground,
            obj.get_status_display(),
        )
