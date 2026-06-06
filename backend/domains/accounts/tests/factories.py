import factory
from factory.django import DjangoModelFactory

from domains.accounts.enums import UserRole
from domains.accounts.models import User


class UserFactory(DjangoModelFactory):
    class Meta:
        model = User

    email = factory.Sequence(lambda n: f"user{n}@example.com")
    username = factory.Sequence(lambda n: f"user{n}")
    role = UserRole.ADVISOR
    is_active = True
    force_password_change = False

    @classmethod
    def _create(cls, model_class, *args, **kwargs):
        password = kwargs.pop("password", "senha@123")
        user = model_class(**kwargs)
        user.set_password(password)
        user.save()
        return user


class AdminFactory(UserFactory):
    role = UserRole.ADMIN
    is_staff = True


class AdvisorFactory(UserFactory):
    role = UserRole.ADVISOR


class RepresentativeFactory(UserFactory):
    role = UserRole.REPRESENTATIVE
    force_password_change = True
