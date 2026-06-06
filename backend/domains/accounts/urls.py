from django.urls import path

from domains.accounts.views import (
    AdminAdvisorDetailView,
    AdminAdvisorView,
    ChangePasswordView,
    ForgotPasswordView,
    LoginView,
    RefreshView,
    ResetPasswordView,
)

urlpatterns = [
    path("auth/login/", LoginView.as_view(), name="auth-login"),
    path("auth/refresh/", RefreshView.as_view(), name="auth-refresh"),
    path("auth/change-password/", ChangePasswordView.as_view(), name="auth-change-password"),
    path("auth/forgot-password/", ForgotPasswordView.as_view(), name="auth-forgot-password"),
    path("auth/reset-password/", ResetPasswordView.as_view(), name="auth-reset-password"),
    path("admin/advisors/", AdminAdvisorView.as_view(), name="admin-advisor-list"),
    path(
        "admin/advisors/<uuid:pk>/", AdminAdvisorDetailView.as_view(), name="admin-advisor-detail"
    ),
]
