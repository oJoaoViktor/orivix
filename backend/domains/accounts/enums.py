from django.db import models


class UserRole(models.TextChoices):
    ADMIN = "admin", "Admin"
    ADVISOR = "advisor", "Orientador"
    REPRESENTATIVE = "representative", "Representante"
