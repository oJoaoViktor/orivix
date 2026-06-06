from rest_framework import serializers

from domains.tenants.models import Domain, Tenant


class TenantSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tenant
        fields = ["id", "name", "schema_name", "created_at"]
        read_only_fields = ["id", "created_at"]


class CreateTenantSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=100)
    schema_name = serializers.SlugField(max_length=63)
    domain = serializers.CharField(max_length=253)

    def validate_schema_name(self, value):
        if Tenant.objects.filter(schema_name=value).exists():
            raise serializers.ValidationError("Já existe uma escola com esse schema.")
        return value

    def validate_domain(self, value):
        if Domain.objects.filter(domain=value).exists():
            raise serializers.ValidationError("Já existe uma escola com esse domínio.")
        return value
