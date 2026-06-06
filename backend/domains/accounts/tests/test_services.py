import pytest

from domains.accounts.services import AuthService
from domains.accounts.tests.factories import AdvisorFactory

pytestmark = pytest.mark.django_db


def test_authenticate_with_valid_email_returns_user():
    user = AdvisorFactory(email="joao@escola.com", password="senha@123")

    result = AuthService.authenticate("joao@escola.com", "senha@123")

    assert result.success is True
    assert result.data == user


def test_authenticate_with_valid_username_returns_user():
    user = AdvisorFactory(username="joao", password="senha@123")

    result = AuthService.authenticate("joao", "senha@123")

    assert result.success is True
    assert result.data == user


def test_authenticate_with_wrong_password_fails():
    AdvisorFactory(email="joao@escola.com", password="senha@123")

    result = AuthService.authenticate("joao@escola.com", "errada")

    assert result.success is False
    assert result.error.code == "INVALID_CREDENTIALS"


def test_authenticate_with_unknown_email_fails():
    result = AuthService.authenticate("ninguem@escola.com", "senha@123")

    assert result.success is False
    assert result.error.code == "INVALID_CREDENTIALS"


def test_authenticate_inactive_user_fails():
    AdvisorFactory(email="joao@escola.com", password="senha@123", is_active=False)

    result = AuthService.authenticate("joao@escola.com", "senha@123")

    assert result.success is False
    assert result.error.code == "INACTIVE_USER"
