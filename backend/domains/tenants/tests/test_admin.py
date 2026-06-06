import pytest
from django.urls import reverse
from rest_framework.test import APIClient

from domains.accounts.tests.factories import AdminFactory, AdvisorFactory
from domains.tenants.models import Tenant

pytestmark = pytest.mark.django_db


@pytest.fixture
def client():
    return APIClient()


@pytest.fixture
def admin():
    return AdminFactory()


@pytest.fixture
def auth_client(client, admin):
    client.force_authenticate(user=admin)
    return client


class TestTenantCreate:
    def test_admin_can_create_tenant(self, auth_client):
        response = auth_client.post(reverse("admin-tenant-list"), {
            "name": "SENAI Campinas",
            "schema_name": "senai_campinas",
            "domain": "senai.localhost",
        })

        assert response.status_code == 201
        assert response.data["name"] == "SENAI Campinas"
        assert Tenant.objects.filter(schema_name="senai_campinas").exists()

    def test_create_tenant_with_duplicate_schema_returns_400(self, auth_client):
        auth_client.post(reverse("admin-tenant-list"), {
            "name": "SENAI Campinas",
            "schema_name": "senai_campinas",
            "domain": "senai.localhost",
        })

        response = auth_client.post(reverse("admin-tenant-list"), {
            "name": "Outra Escola",
            "schema_name": "senai_campinas",
            "domain": "outra.localhost",
        })

        assert response.status_code == 400

    def test_non_admin_cannot_create_tenant(self, client):
        advisor = AdvisorFactory()
        client.force_authenticate(user=advisor)

        response = client.post(reverse("admin-tenant-list"), {
            "name": "SENAI Campinas",
            "schema_name": "senai_campinas",
            "domain": "senai.localhost",
        })

        assert response.status_code == 403

    def test_unauthenticated_cannot_create_tenant(self, client):
        response = client.post(reverse("admin-tenant-list"), {
            "name": "SENAI Campinas",
            "schema_name": "senai_campinas",
            "domain": "senai.localhost",
        })

        assert response.status_code == 401


class TestTenantList:
    def test_admin_can_list_tenants(self, auth_client):
        response = auth_client.get(reverse("admin-tenant-list"))

        assert response.status_code == 200

    def test_non_admin_cannot_list_tenants(self, client):
        advisor = AdvisorFactory()
        client.force_authenticate(user=advisor)

        response = client.get(reverse("admin-tenant-list"))

        assert response.status_code == 403
