"""URLs for the users app."""

from django.urls import path

from . import views

app_name = "users"
urlpatterns = [
    path("users/", views.UserListView.as_view()),
    path("users/<int:pk>/", views.UserListView.as_view()),
    path("users/logout/", views.LogoutView.as_view()),
]
