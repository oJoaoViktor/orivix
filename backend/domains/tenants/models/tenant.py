from django.db import models
from django_tenants.models import TenantMixin
from shared.utils import generate_uuid7


class Tenant(TenantMixin):
    id = models.UUIDField(primary_key=True, default=generate_uuid7, editable=False)
    name = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)

    auto_create_schema = True

    class Meta:
        verbose_name = "Escola"
        verbose_name_plural = "Escolas"

    def __str__(self):
        return self.name
