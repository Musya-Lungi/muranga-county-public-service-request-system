
from django.conf import settings
from django.db import models
from django.utils import timezone
import uuid


class ServiceRequest(models.Model):
    class Category(models.TextChoices):
        WATER = "WATER", "Water Supply"
        ROADS = "ROADS", "Roads and Potholes"
        LIGHTING = "LIGHTING", "Street Lighting"
        WASTE = "WASTE", "Garbage Collection"
        DRAINAGE = "DRAINAGE", "Drainage and Flooding"
        PUBLIC_HEALTH = "HEALTH", "Public Health"
        OTHER = "OTHER", "Other"

    class Status(models.TextChoices):
        PENDING = "PENDING", "Pending"
        IN_PROGRESS = "IN_PROGRESS", "In Progress"
        RESOLVED = "RESOLVED", "Resolved"

    reference_number = models.UUIDField(
        default=uuid.uuid4,
        unique=True,
        editable=False,
    )
    citizen = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="service_requests",
    )
    category = models.CharField(
        max_length=20,
        choices=Category.choices,
    )
    title = models.CharField(max_length=120)
    description = models.TextField()
    location = models.CharField(max_length=255)
    image = models.ImageField(
        upload_to="service_requests/",
        blank=True,
        null=True,
    )
    status = models.CharField(
        max_length=20,
        choices=Status.choices,
        default=Status.PENDING,
    )
    created_at = models.DateTimeField(default=timezone.now, editable=False)
    updated_at = models.DateTimeField(auto_now=True)
    resolved_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        ordering = ["-created_at"]
        indexes = [
            models.Index(fields=["status", "created_at"]),
            models.Index(fields=["category", "status"]),
        ]




    def save(self, *args, **kwargs):
        if self.status == self.Status.RESOLVED:
            if self.resolved_at is None:
                self.resolved_at = timezone.now()
        else:
            self.resolved_at = None

        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.get_category_display()} — {self.reference_number}"




