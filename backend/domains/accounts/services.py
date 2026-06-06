from django.conf import settings
from django.core.mail import send_mail

from domains.accounts.repositories import UserRepository
from shared.exceptions import Result


class AuthService:
    @staticmethod
    def authenticate(email_or_username: str, password: str) -> Result:
        if "@" in email_or_username:
            user = UserRepository.get_by_email(email_or_username)
        else:
            user = UserRepository.get_by_username(email_or_username)
        if user is None:
            return Result.fail("INVALID_CREDENTIALS", "Email, username ou senha inválidos.")

        if not user.is_active:
            return Result.fail("INACTIVE_USER", "Usuário inativo.")

        if not user.check_password(password):
            return Result.fail("INVALID_CREDENTIALS", "Email, username ou senha inválidos.")

        return Result.ok(user)

    @staticmethod
    def send_password_reset_email(user, uid: str, token: str) -> None:
        reset_url = f"{settings.FRONTEND_URL}/reset-password?uid={uid}&token={token}"
        send_mail(
            subject="Redefina sua senha — Orivix",
            message=f"Clique no link para redefinir sua senha:\n\n{reset_url}",
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[user.email],
        )
