
from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse

from .models import ServiceRequest


class CitizenRequestPrivacyTests(TestCase):
    def setUp(self):
        self.citizen_one = User.objects.create_user(
            username="citizen_one",
            password="TestPassword123!",
        )
        self.citizen_two = User.objects.create_user(
            username="citizen_two",
            password="TestPassword123!",
        )

        self.request_one = ServiceRequest.objects.create(
            citizen=self.citizen_one,
            category=ServiceRequest.Category.WATER,
            title="Water supply issue",
            description="No water in our area.",
            location="Kangeta",
        )

        self.request_two = ServiceRequest.objects.create(
            citizen=self.citizen_two,
            category=ServiceRequest.Category.ROADS,
            title="Damaged road",
            description="There are potholes on the road.",
            location="Murang'a",
        )

    def test_citizen_sees_only_their_own_requests(self):
        self.client.force_login(self.citizen_one)

        response = self.client.get(reverse("my_requests"))

        self.assertEqual(response.status_code, 200)

        displayed_requests = list(
            response.context["service_requests"]
        )

        self.assertEqual(displayed_requests, [self.request_one])
        self.assertNotIn(self.request_two, displayed_requests)

    def test_anonymous_user_cannot_access_submit_request(self):
        response = self.client.get(
            reverse("submit_request")
        )

        self.assertEqual(response.status_code, 302)
        self.assertIn("/accounts/login/", response.url)


    def test_new_request_defaults_to_pending(self):
        self.assertEqual(
            self.request_one.status,
            ServiceRequest.Status.PENDING,
        )

    def test_resolution_timestamp_tracks_status(self):
        self.request_one.status = ServiceRequest.Status.RESOLVED
        self.request_one.save()

        self.assertIsNotNone(self.request_one.resolved_at)

        self.request_one.status = ServiceRequest.Status.IN_PROGRESS
        self.request_one.save()

        self.assertIsNone(self.request_one.resolved_at)

    def test_homepage_analytics_counts_requests_correctly(self):
        self.request_one.status = ServiceRequest.Status.RESOLVED
        self.request_one.save()

        response = self.client.get(reverse("home"))

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context["total_requests"], 2)
        self.assertEqual(response.context["open_requests"], 1)
        self.assertEqual(response.context["resolved_requests"], 1)

    def test_anonymous_user_cannot_create_request(self):
        response = self.client.post(
            reverse("submit_request"),
            {
                "category": ServiceRequest.Category.WATER,
                "title": "Unauthorized request",
                "description": "Testing anonymous submission.",
                "location": "Kangeta",
            },
        )

        self.assertEqual(response.status_code, 302)
        self.assertEqual(ServiceRequest.objects.count(), 2)

    def test_registration_page_loads_for_anonymous_user(self):
        response = self.client.get(reverse("register"))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "username")
        self.assertContains(response, "password")


    def test_login_page_loads_for_anonymous_user(self):
        response = self.client.get(reverse("login"))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "username")
        self.assertContains(response, "password")


    def test_citizen_can_register_successfully(self):
        response = self.client.post(
            reverse("register"),
            {
                "username": "new_citizen",
                "email": "new_citizen@example.com",
                "password1": "SafeTestPass123!",
                "password2": "SafeTestPass123!",
            },
        )

        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse("login"))
        self.assertTrue(
            User.objects.filter(username="new_citizen").exists()
        )


    def test_citizen_can_log_in_successfully(self):
        response = self.client.post(
            reverse("login"),
            {
                "username": "citizen_one",
                "password": "TestPassword123!",
            },
        )

        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse("home"))
        self.assertEqual(
            int(self.client.session["_auth_user_id"]),
            self.citizen_one.pk,
        )

    def test_citizen_can_submit_request_successfully(self):
        self.client.force_login(self.citizen_one)

        response = self.client.post(
            reverse("submit_request"),
            {
                "category": ServiceRequest.Category.WATER,
                "title": "Broken water pipe",
                "description": "A water pipe is leaking.",
                "location": "Kangeta",
            },
        )

        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse("home"))

        created_request = ServiceRequest.objects.get(
            title="Broken water pipe"
        )

        self.assertEqual(
            created_request.citizen,
            self.citizen_one,
        )
        self.assertEqual(
            created_request.status,
            ServiceRequest.Status.PENDING,
        )

    def test_request_status_workflow(self):
        self.assertEqual(
            self.request_one.status,
            ServiceRequest.Status.PENDING,
        )

        self.request_one.status = ServiceRequest.Status.IN_PROGRESS
        self.request_one.save()
        self.request_one.refresh_from_db()

        self.assertEqual(
            self.request_one.status,
            ServiceRequest.Status.IN_PROGRESS,
        )

        self.request_one.status = ServiceRequest.Status.RESOLVED
        self.request_one.save()
        self.request_one.refresh_from_db()

        self.assertEqual(
            self.request_one.status,
            ServiceRequest.Status.RESOLVED,
        )
        self.assertIsNotNone(self.request_one.resolved_at)

    def test_invalid_request_is_rejected(self):
        self.client.force_login(self.citizen_one)

        response = self.client.post(
            reverse("submit_request"),
            {
                "category": ServiceRequest.Category.WATER,
                "title": "",
                "description": "",
                "location": "",
            },
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(ServiceRequest.objects.count(), 2)
        self.assertTrue(response.context["form"].errors)
