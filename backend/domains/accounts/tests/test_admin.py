import pytest
from django.urls import reverse
from rest_framework.test import APIClient

from domains.accounts.tests.factories import AdminFactory, AdvisorFactory

pytestmark = pytest.mark.django_db


@pytest.fixture
def client():
    return APIClient()


@pytest.fixture
def admin():
    return AdminFactory()


@pytest.fixture
def auth_client(client, admin):
    client.force_authenticate(user=admin)
    return client


class TestAdvisorCreate:
    def test_admin_can_create_advisor(self, auth_client):
        response = auth_client.post(
            reverse("admin-advisor-list"),
            {
                "email": "advisor@escola.com",
                "username": "advisor1",
            },
        )

        assert response.status_code == 201
        assert response.data["email"] == "advisor@escola.com"
        assert response.data["role"] == "advisor"

    def test_created_advisor_has_force_password_change(self, auth_client):
        auth_client.post(
            reverse("admin-advisor-list"),
            {
                "email": "advisor@escola.com",
                "username": "advisor1",
            },
        )

        from domains.accounts.models import User

        user = User.objects.get(email="advisor@escola.com")
        assert user.force_password_change is True

    def test_create_advisor_with_duplicate_email_returns_400(self, auth_client):
        AdvisorFactory(email="advisor@escola.com")

        response = auth_client.post(
            reverse("admin-advisor-list"),
            {
                "email": "advisor@escola.com",
                "username": "outro",
            },
        )

        assert response.status_code == 400

    def test_non_admin_cannot_create_advisor(self, client):
        advisor = AdvisorFactory()
        client.force_authenticate(user=advisor)

        response = client.post(
            reverse("admin-advisor-list"),
            {
                "email": "novo@escola.com",
                "username": "novo",
            },
        )

        assert response.status_code == 403

    def test_unauthenticated_cannot_create_advisor(self, client):
        response = client.post(
            reverse("admin-advisor-list"),
            {
                "email": "novo@escola.com",
                "username": "novo",
            },
        )

        assert response.status_code == 401


class TestAdvisorList:
    def test_admin_can_list_advisors(self, auth_client):
        AdvisorFactory.create_batch(3)

        response = auth_client.get(reverse("admin-advisor-list"))

        assert response.status_code == 200
        assert len(response.data) == 3

    def test_non_admin_cannot_list_advisors(self, client):
        advisor = AdvisorFactory()
        client.force_authenticate(user=advisor)

        response = client.get(reverse("admin-advisor-list"))

        assert response.status_code == 403


class TestAdvisorToggleActive:
    def test_admin_can_deactivate_advisor(self, auth_client):
        advisor = AdvisorFactory()

        response = auth_client.patch(
            reverse("admin-advisor-detail", args=[advisor.id]),
            {"is_active": False},
        )

        assert response.status_code == 200
        advisor.refresh_from_db()
        assert advisor.is_active is False

    def test_admin_can_reactivate_advisor(self, auth_client):
        advisor = AdvisorFactory(is_active=False)

        response = auth_client.patch(
            reverse("admin-advisor-detail", args=[advisor.id]),
            {"is_active": True},
        )

        assert response.status_code == 200
        advisor.refresh_from_db()
        assert advisor.is_active is True

    def test_non_admin_cannot_toggle_advisor(self, client):
        advisor = AdvisorFactory()
        client.force_authenticate(user=advisor)

        response = client.patch(
            reverse("admin-advisor-detail", args=[advisor.id]),
            {"is_active": False},
        )

        assert response.status_code == 403
