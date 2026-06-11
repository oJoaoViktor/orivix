import pytest
from django.urls import reverse
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from rest_framework.test import APIClient

from domains.accounts.tests.factories import AdvisorFactory
from domains.accounts.tokens import password_reset_token

pytestmark = pytest.mark.django_db


@pytest.fixture
def client():
    return APIClient()


@pytest.fixture
def advisor():
    return AdvisorFactory(email="advisor@example.com", password="password@123")


class TestLogin:
    def test_login_with_email_returns_tokens(self, client, advisor):
        response = client.post(
            reverse("auth-login"),
            {
                "credential": "advisor@example.com",
                "password": "password@123",
            },
        )

        assert response.status_code == 200
        assert "access" in response.data
        assert "refresh" in response.data

    def test_login_with_username_returns_tokens(self, client):
        AdvisorFactory(username="advisor", password="password@123")

        response = client.post(
            reverse("auth-login"),
            {
                "credential": "advisor",
                "password": "password@123",
            },
        )

        assert response.status_code == 200
        assert "access" in response.data

    def test_login_with_wrong_password_returns_401(self, client, advisor):
        response = client.post(
            reverse("auth-login"),
            {
                "credential": "advisor@example.com",
                "password": "wrong-password",
            },
        )

        assert response.status_code == 401

    def test_login_with_inactive_user_returns_403(self, client):
        AdvisorFactory(email="advisor@example.com", password="password@123", is_active=False)

        response = client.post(
            reverse("auth-login"),
            {
                "credential": "advisor@example.com",
                "password": "password@123",
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
                "credential": "advisor@example.com",
                "password": "password@123",
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
                "current_password": "password@123",
                "new_password": "newPassword@456",
            },
        )

        assert response.status_code == 200
        advisor.refresh_from_db()
        assert advisor.check_password("newPassword@456")
        assert advisor.force_password_change is False

    def test_change_password_with_wrong_current_password_returns_400(self, client, advisor):
        client.force_authenticate(user=advisor)

        response = client.post(
            reverse("auth-change-password"),
            {
                "current_password": "wrong-password",
                "new_password": "newPassword@456",
            },
        )

        assert response.status_code == 400

    def test_change_password_requires_authentication(self, client):
        response = client.post(
            reverse("auth-change-password"),
            {
                "current_password": "password@123",
                "new_password": "newPassword@456",
            },
        )

        assert response.status_code == 401


class TestForgotPassword:
    def test_returns_200_when_email_exists(self, client, mailoutbox, advisor):
        response = client.post(
            reverse("auth-forgot-password"),
            {"email": "advisor@example.com"},
        )

        assert response.status_code == 200

    def test_returns_200_when_email_does_not_exist(self, client, mailoutbox):
        response = client.post(
            reverse("auth-forgot-password"),
            {"email": "unknown@example.com"},
        )

        assert response.status_code == 200

    def test_sends_email_when_user_exists(self, client, mailoutbox, advisor):
        client.post(
            reverse("auth-forgot-password"),
            {"email": "advisor@example.com"},
        )

        assert len(mailoutbox) == 1
        assert mailoutbox[0].to == ["advisor@example.com"]

    def test_does_not_send_email_when_user_not_found(self, client, mailoutbox):
        client.post(
            reverse("auth-forgot-password"),
            {"email": "unknown@example.com"},
        )

        assert len(mailoutbox) == 0

    def test_missing_email_returns_400(self, client):
        response = client.post(reverse("auth-forgot-password"), {})

        assert response.status_code == 400


class TestResetPassword:
    @pytest.fixture
    def reset_credentials(self, advisor):
        uid = urlsafe_base64_encode(force_bytes(advisor.pk))
        token = password_reset_token.make_token(advisor)
        return uid, token

    def test_valid_credentials_return_200(self, client, reset_credentials):
        uid, token = reset_credentials

        response = client.post(
            reverse("auth-reset-password"),
            {"uid": uid, "token": token, "new_password": "newPassword@456"},
        )

        assert response.status_code == 200

    def test_valid_credentials_change_password(self, client, advisor, reset_credentials):
        uid, token = reset_credentials

        client.post(
            reverse("auth-reset-password"),
            {"uid": uid, "token": token, "new_password": "newPassword@456"},
        )

        advisor.refresh_from_db()
        assert advisor.check_password("newPassword@456")

    def test_clears_force_password_change_flag(self, client):
        user = AdvisorFactory(force_password_change=True)
        uid = urlsafe_base64_encode(force_bytes(user.pk))
        token = password_reset_token.make_token(user)

        client.post(
            reverse("auth-reset-password"),
            {"uid": uid, "token": token, "new_password": "newPassword@456"},
        )

        user.refresh_from_db()
        assert user.force_password_change is False

    def test_invalid_token_returns_400(self, client, reset_credentials):
        uid, _ = reset_credentials

        response = client.post(
            reverse("auth-reset-password"),
            {"uid": uid, "token": "invalid-token", "new_password": "newPassword@456"},
        )

        assert response.status_code == 400

    def test_invalid_uid_returns_400(self, client, reset_credentials):
        _, token = reset_credentials

        response = client.post(
            reverse("auth-reset-password"),
            {"uid": "invalid-uid", "token": token, "new_password": "newPassword@456"},
        )

        assert response.status_code == 400

    def test_missing_fields_returns_400(self, client):
        response = client.post(reverse("auth-reset-password"), {})

        assert response.status_code == 400
