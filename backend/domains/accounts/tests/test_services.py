import pytest
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode

from domains.accounts.services import AuthService
from domains.accounts.tests.factories import AdvisorFactory
from domains.accounts.tokens import password_reset_token

pytestmark = pytest.mark.django_db


def test_authenticate_with_valid_email_returns_user():
    user = AdvisorFactory(email="advisor@example.com", password="password@123")

    result = AuthService.authenticate("advisor@example.com", "password@123")

    assert result.success is True
    assert result.data == user


def test_authenticate_with_valid_username_returns_user():
    user = AdvisorFactory(username="advisor", password="password@123")

    result = AuthService.authenticate("advisor", "password@123")

    assert result.success is True
    assert result.data == user


def test_authenticate_with_wrong_password_fails():
    AdvisorFactory(email="advisor@example.com", password="password@123")

    result = AuthService.authenticate("advisor@example.com", "errada")

    assert result.success is False
    assert result.error.code == "INVALID_CREDENTIALS"


def test_authenticate_with_unknown_email_fails():
    result = AuthService.authenticate("unknown@example.com", "password@123")

    assert result.success is False
    assert result.error.code == "INVALID_CREDENTIALS"


def test_authenticate_inactive_user_fails():
    AdvisorFactory(email="advisor@example.com", password="password@123", is_active=False)

    result = AuthService.authenticate("advisor@example.com", "password@123")

    assert result.success is False
    assert result.error.code == "INACTIVE_USER"


def test_send_password_reset_email_sends_to_correct_address(mailoutbox):
    user = AdvisorFactory(email="advisor@example.com")
    uid = urlsafe_base64_encode(force_bytes(user.pk))
    token = password_reset_token.make_token(user)

    AuthService.send_password_reset_email(user, uid, token)

    assert len(mailoutbox) == 1
    assert mailoutbox[0].to == ["advisor@example.com"]


def test_send_password_reset_email_has_correct_subject(mailoutbox):
    user = AdvisorFactory()
    uid = urlsafe_base64_encode(force_bytes(user.pk))
    token = password_reset_token.make_token(user)

    AuthService.send_password_reset_email(user, uid, token)

    assert mailoutbox[0].subject == "Redefina sua senha — Orivix"


def test_send_password_reset_email_html_contains_unencoded_url(mailoutbox, settings):
    settings.FRONTEND_URL = "http://testserver"
    user = AdvisorFactory()
    uid = urlsafe_base64_encode(force_bytes(user.pk))
    token = password_reset_token.make_token(user)

    AuthService.send_password_reset_email(user, uid, token)

    expected_url = f"http://testserver/reset-password?uid={uid}&token={token}"
    html_body = mailoutbox[0].alternatives[0][0]
    assert expected_url in html_body
