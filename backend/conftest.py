import pytest


@pytest.fixture(scope="session")
def django_db_setup(django_test_environment, django_db_blocker):
    with django_db_blocker.unblock():
        from django.db import connection
        from domains.tenants.models import Domain, Tenant

        connection.set_schema_to_public()

        tenant, _ = Tenant.objects.get_or_create(
            schema_name="public",
            defaults={"name": "Public"},
        )
        Domain.objects.get_or_create(
            domain="testserver",
            defaults={"tenant": tenant, "is_primary": True},
        )
