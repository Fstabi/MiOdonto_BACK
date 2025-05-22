from django.test import TestCase  # type: ignore
from django.contrib.auth import get_user_model  # type: ignore
from django.urls import reverse  # type: ignore
from django.test import Client  # type: ignore

class CustomUserAdminTests(TestCase):
    """Test for Django admin."""

    def setUp(self):
        """Create user and client."""
        self.client = Client()
        self.admin_user = get_user_model().objects.create_superuser(
            username="admin",
            email="admin@example.com",
            password="testpass123",
        )
        self.client.force_login(self.admin_user)
        self.user = get_user_model().objects.create_user(
            email="user@example.com",
            password="testpass123",
            username="testuser",
        )

    def test_user_listed(self):
        """Test that users are listed on user page."""
        url = reverse("admin:core_customuser_changelist")
        res = self.client.get(url)

        self.assertContains(res, self.user.username)
        self.assertContains(res, self.user.email)