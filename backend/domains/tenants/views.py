from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from domains.accounts.permissions import IsAdminRole
from domains.tenants.models import Tenant
from domains.tenants.serializers import CreateTenantSerializer, TenantSerializer
from domains.tenants.services import TenantService


class AdminTenantView(APIView):
    permission_classes = [IsAdminRole]

    def get(self, request):
        tenants = Tenant.objects.exclude(schema_name="public")
        serializer = TenantSerializer(tenants, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = CreateTenantSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        result = TenantService.create_tenant(
            name=serializer.validated_data["name"],
            schema_name=serializer.validated_data["schema_name"],
            domain=serializer.validated_data["domain"],
        )

        return Response(TenantSerializer(result.data).data, status=status.HTTP_201_CREATED)
