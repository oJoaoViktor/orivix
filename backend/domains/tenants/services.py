from shared.exceptions import Result

from domains.tenants.models import Domain, Tenant


class TenantService:
    @staticmethod
    def create_tenant(name: str, schema_name: str, domain: str) -> Result:
        tenant = Tenant(name=name, schema_name=schema_name)
        tenant.save()

        Domain.objects.create(
            tenant=tenant,
            domain=domain,
            is_primary=True,
        )

        return Result.ok(tenant)
