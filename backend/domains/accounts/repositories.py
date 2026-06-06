from domains.accounts.models import User


class UserRepository:
    @staticmethod
    def get_by_id(user_id) -> User | None:
        return User.objects.filter(id=user_id).first()

    @staticmethod
    def get_by_email(email: str) -> User | None:
        return User.objects.filter(email=email).first()

    @staticmethod
    def get_by_username(username: str) -> User | None:
        return User.objects.filter(username=username).first()

    @staticmethod
    def email_exists(email: str) -> bool:
        return User.objects.filter(email=email).exists()

    @staticmethod
    def username_exists(username: str) -> bool:
        return User.objects.filter(username=username).exists()
