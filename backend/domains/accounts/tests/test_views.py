import pytest
from django.urls import reverse
from rest_framework.test import APIClient

from domains.accounts.tests.factories import AdvisorFactory

pytestmark = pytest.mark.django_db


@pytest.fixture
def client():
    return APIClient()


@pytest.fixture
def advisor():
    return AdvisorFactory(email="joao@escola.com", password="senha@123")


class TestLogin:
    def test_login_with_email_returns_tokens(self, client, advisor):
        response = client.post(
            reverse("auth-login"),
            {
                "credential": "joao@escola.com",
                "password": "senha@123",
            },
        )

        assert response.status_code == 200
        assert "access" in response.data
        assert "refresh" in response.data

    def test_login_with_username_returns_tokens(self, client):
        AdvisorFactory(username="joao", password="senha@123")

        response = client.post(
            reverse("auth-login"),
            {
                "credential": "joao",
                "password": "senha@123",
            },
        )

        assert response.status_code == 200
        assert "access" in response.data

    def test_login_with_wrong_password_returns_401(self, client, advisor):
        response = client.post(
            reverse("auth-login"),
            {
                "credential": "joao@escola.com",
                "password": "errada",
            },
        )

        assert response.status_code == 401

    def test_login_with_inactive_user_returns_403(self, client):
        AdvisorFactory(email="joao@escola.com", password="senha@123", is_active=False)

        response = client.post(
            reverse("auth-login"),
            {
                "credential": "joao@escola.com",
                "password": "senha@123",
            },
        )

        assert response.status_code == 403

    def test_login_missing_fields_returns_400(self, client):
        response = client.post(reverse("auth-login"), {})

        assert response.status_code == 400


class TestRefresh:
    def test_refresh_returns_new_access_token(self, client, advisor):
        login = client.post(
            reverse("auth-login"),
            {
                "credential": "joao@escola.com",
                "password": "senha@123",
            },
        )
        refresh_token = login.data["refresh"]

        response = client.post(reverse("auth-refresh"), {"refresh": refresh_token})

        assert response.status_code == 200
        assert "access" in response.data

    def test_refresh_with_invalid_token_returns_401(self, client):
        response = client.post(reverse("auth-refresh"), {"refresh": "token-invalido"})

        assert response.status_code == 401


class TestChangePassword:
    def test_change_password_succeeds(self, client, advisor):
        client.force_authenticate(user=advisor)

        response = client.post(
            reverse("auth-change-password"),
            {
                "current_password": "senha@123",
                "new_password": "novaSenha@456",
            },
        )

        assert response.status_code == 200
        advisor.refresh_from_db()
        assert advisor.check_password("novaSenha@456")
        assert advisor.force_password_change is False

    def test_change_password_with_wrong_current_password_returns_400(self, client, advisor):
        client.force_authenticate(user=advisor)

        response = client.post(
            reverse("auth-change-password"),
            {
                "current_password": "errada",
                "new_password": "novaSenha@456",
            },
        )

        assert response.status_code == 400

    def test_change_password_requires_authentication(self, client):
        response = client.post(
            reverse("auth-change-password"),
            {
                "current_password": "senha@123",
                "new_password": "novaSenha@456",
            },
        )

        assert response.status_code == 401
