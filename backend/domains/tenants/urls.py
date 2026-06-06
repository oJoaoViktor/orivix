from django.urls import path

from domains.tenants.views import AdminTenantView

urlpatterns = [
    path("admin/tenants/", AdminTenantView.as_view(), name="admin-tenant-list"),
]
