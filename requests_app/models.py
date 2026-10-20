
"""
Database models for the Murang'a County Public Service Request System.

This module defines the ServiceRequest model used to store citizen
complaints and service requests, track their progress, and record
when a request is resolved.
"""

import uuid

from django.conf import settings
from django.db import models
from django.utils import timezone


class ServiceRequest(models.Model):
    """Represent a service request submitted by a registered citizen."""

    # Controlled categories keep submitted requests consistent and easier
    # for county administrators to classify and manage.
    class Category(models.TextChoices):
        WATER = "WATER", "Water Supply"
        ROADS = "ROADS", "Roads and Potholes"
        LIGHTING = "LIGHTING", "Street Lighting"
        WASTE = "WASTE", "Garbage Collection"
        DRAINAGE = "DRAINAGE", "Drainage and Flooding"
        PUBLIC_HEALTH = "HEALTH", "Public Health"
        OTHER = "OTHER", "Other"

    # Define the permitted stages in the request-processing workflow.
    class Status(models.TextChoices):
        PENDING = "PENDING", "Pending"
        IN_PROGRESS = "IN_PROGRESS", "In Progress"
        RESOLVED = "RESOLVED", "Resolved"

    # Generate a unique public reference for each request.
    # UUIDs are not sequential and cannot be edited through model forms.
    reference_number = models.UUIDField(
        default=uuid.uuid4,
        unique=True,
        editable=False,
    )

    # Link each request to the user who submitted it.
    # CASCADE means deleting that user also deletes their requests.
    # The related_name enables access through user.service_requests.
    citizen = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="service_requests",
    )

    # Store the request classification using the predefined choices above.
    category = models.CharField(
        max_length=20,
        choices=Category.choices,
    )

    # Store a short summary and a fuller explanation of the reported issue.
    title = models.CharField(max_length=120)
    description = models.TextField()

    # Record where the reported service issue is located.
    location = models.CharField(max_length=255)

    # Allow citizens to attach an optional image as supporting evidence.
    # Uploaded files are stored under the service_requests media directory.
    image = models.ImageField(
        upload_to="service_requests/",
        blank=True,
        null=True,
    )

    # Track the request's current processing stage.
    # New requests start as pending until an administrator updates the status.
    status = models.CharField(
        max_length=20,
        choices=Status.choices,
        default=Status.PENDING,
    )

    # Record creation and modification times for tracking and reporting.
    # The creation timestamp cannot be edited through model forms.
    created_at = models.DateTimeField(default=timezone.now, editable=False)
    updated_at = models.DateTimeField(auto_now=True)

    # Store the resolution time when a request is resolved.
    # This field remains empty for unresolved requests.
    resolved_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        """Configure default ordering and database indexes."""

        # Display the newest requests first in standard query results.
        ordering = ["-created_at"]

        # Index frequently useful combinations to support filtering and
        # reporting by status, category, and creation time.
        indexes = [
            models.Index(fields=["status", "created_at"]),
            models.Index(fields=["category", "status"]),
        ]

    def save(self, *args, **kwargs):
        """Keep the resolution timestamp consistent with the request status."""

        # Set the resolution time the first time the request is saved
        # with a resolved status, unless a timestamp already exists.
        if self.status == self.Status.RESOLVED:
            if self.resolved_at is None:
                self.resolved_at = timezone.now()
        else:
            # Clear the resolution timestamp if the request is no longer
            # resolved, so the timestamp reflects the current status.
            self.resolved_at = None

        # Preserve Django's normal save behaviour after applying the rule.
        super().save(*args, **kwargs)

    def __str__(self):
        """Return a readable representation for the admin and shell."""
        return f"{self.title} — {self.reference_number}"
