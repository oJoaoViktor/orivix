import secrets

from django.conf import settings
from django.core.mail import send_mail

from domains.accounts.enums import UserRole
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
    def create_advisor(email: str, username: str) -> Result:
        if UserRepository.email_exists(email):
            return Result.fail("EMAIL_TAKEN", "Este email já está em uso.")
        if UserRepository.username_exists(username):
            return Result.fail("USERNAME_TAKEN", "Este username já está em uso.")

        temporary_password = secrets.token_urlsafe(12)

        from domains.accounts.models import User
        user = User.objects.create_user(
            email=email,
            username=username,
            password=temporary_password,
            role=UserRole.ADVISOR,
            force_password_change=True,
        )

        AuthService._send_welcome_email(user, temporary_password)
        return Result.ok(user)

    @staticmethod
    def _send_welcome_email(user, temporary_password: str) -> None:
        send_mail(
            subject="Bem-vindo ao Orivix — suas credenciais de acesso",
            message=(
                f"Olá!\n\n"
                f"Sua conta foi criada.\n\n"
                f"Email: {user.email}\n"
                f"Senha temporária: {temporary_password}\n\n"
                f"Acesse {settings.FRONTEND_URL} e altere sua senha no primeiro login."
            ),
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[user.email],
        )

    @staticmethod
    def send_password_reset_email(user, uid: str, token: str) -> None:
        reset_url = f"{settings.FRONTEND_URL}/reset-password?uid={uid}&token={token}"
        send_mail(
            subject="Redefina sua senha — Orivix",
            message=f"Clique no link para redefinir sua senha:\n\n{reset_url}",
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[user.email],
        )
