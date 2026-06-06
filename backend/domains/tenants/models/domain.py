from django.db import models
from django_tenants.models import DomainMixin
from shared.utils import generate_uuid7


class Domain(DomainMixin):
    id = models.UUIDField(primary_key=True, default=generate_uuid7, editable=False)

    class Meta:
        verbose_name = "Domínio"
        verbose_name_plural = "Domínios"

    def __str__(self):
        return self.domain
