"""Admins URL Configuration."""

from django.urls import path

from . import views

app_name = "admins"

urlpatterns = [
    path("admins/", views.AdminListView.as_view()),
    path("admins/<int:pk>/", views.AdminDetailView.as_view()),
]
