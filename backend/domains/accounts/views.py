from django.utils.encoding import force_bytes, force_str
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from rest_framework import status
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken

from domains.accounts.repositories import UserRepository
from domains.accounts.serializers import (
    ChangePasswordSerializer,
    ForgotPasswordSerializer,
    LoginSerializer,
    ResetPasswordSerializer,
)
from domains.accounts.services import AuthService
from domains.accounts.tokens import password_reset_token


class LoginView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        result = AuthService.authenticate(
            serializer.validated_data["credential"],
            serializer.validated_data["password"],
        )

        if not result.success:
            if result.error.code == "INACTIVE_USER":
                return Response({"detail": result.error.message}, status=status.HTTP_403_FORBIDDEN)
            return Response({"detail": result.error.message}, status=status.HTTP_401_UNAUTHORIZED)

        refresh = RefreshToken.for_user(result.data)
        return Response({
            "access": str(refresh.access_token),
            "refresh": str(refresh),
        })


class RefreshView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        from rest_framework_simplejwt.exceptions import TokenError
        from rest_framework_simplejwt.tokens import RefreshToken

        token = request.data.get("refresh")
        if not token:
            return Response({"detail": "Refresh token é obrigatório."}, status=status.HTTP_401_UNAUTHORIZED)

        try:
            refresh = RefreshToken(token)
            return Response({"access": str(refresh.access_token)})
        except TokenError:
            return Response({"detail": "Token inválido ou expirado."}, status=status.HTTP_401_UNAUTHORIZED)


class ChangePasswordView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = ChangePasswordSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = request.user
        if not user.check_password(serializer.validated_data["current_password"]):
            return Response(
                {"detail": "Senha atual incorreta."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        user.set_password(serializer.validated_data["new_password"])
        user.force_password_change = False
        user.save(update_fields=["password", "force_password_change"])
        return Response({"detail": "Senha alterada com sucesso."})


class ForgotPasswordView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = ForgotPasswordSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = UserRepository.get_by_email(serializer.validated_data["email"])
        if user:
            uid = urlsafe_base64_encode(force_bytes(user.pk))
            token = password_reset_token.make_token(user)
            AuthService.send_password_reset_email(user, uid, token)

        # sempre retorna 200 para não revelar se o email existe
        return Response({"detail": "Se o email existir, você receberá um link de redefinição."})


class ResetPasswordView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = ResetPasswordSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        try:
            uid = force_str(urlsafe_base64_decode(serializer.validated_data["uid"]))
            user = UserRepository.get_by_id(uid)
        except Exception:
            user = None

        if not user or not password_reset_token.check_token(user, serializer.validated_data["token"]):
            return Response({"detail": "Link inválido ou expirado."}, status=status.HTTP_400_BAD_REQUEST)

        user.set_password(serializer.validated_data["new_password"])
        user.force_password_change = False
        user.save(update_fields=["password", "force_password_change"])
        return Response({"detail": "Senha redefinida com sucesso."})
