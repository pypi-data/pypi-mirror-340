"""Authentication URL Configuration."""

from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView

from . import views as auth_view

urlpatterns = [
    path("patient/auth/login", auth_view.PatientLoginView.as_view()),
    path("patient/auth/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path("admins/auth/login", auth_view.AdminLoginView.as_view()),
    path("admins/auth/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path("practitioners/auth/login", auth_view.PractitionerLoginView.as_view()),
    path(
        "practitioners/auth/refresh/", TokenRefreshView.as_view(), name="token_refresh"
    ),
]
