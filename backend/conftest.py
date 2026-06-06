import pytest


@pytest.fixture(scope="session")
def django_db_setup(django_test_environment, django_db_blocker):
    with django_db_blocker.unblock():
        from django.core.management import call_command
        from django.db import connection
        from domains.tenants.models import Domain, Tenant

        call_command("migrate_schemas", "--shared", verbosity=0)

        connection.set_schema_to_public()

        tenant, _ = Tenant.objects.get_or_create(
            schema_name="public",
            defaults={"name": "Public"},
        )
        Domain.objects.get_or_create(
            domain="testserver",
            defaults={"tenant": tenant, "is_primary": True},
        )
