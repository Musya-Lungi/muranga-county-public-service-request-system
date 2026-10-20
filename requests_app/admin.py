from django.contrib import admin
from .models import ServiceRequest


@admin.register(ServiceRequest)
class ServiceRequestAdmin(admin.ModelAdmin):
    list_display = (
        "reference_number",
        "category",
        "title",
        "citizen",
        "status",
        "created_at",
    )
    list_filter = ("status", "category", "created_at")
    search_fields = (
        "title",
        "description",
        "location",
        "citizen__username",
    )
    readonly_fields = (
        "reference_number",
        "created_at",
        "updated_at",
    )
    ordering = ("-created_at",)