"""transport urls."""

from django.urls import path

from nebula.transports import views

app_name = "transports"

urlpatterns = [
    path("transports/", views.TransportListView.as_view(), name="transport-list"),
    path(
        "transports/<int:pk>/",
        views.TransportDetailView.as_view(),
        name="transport-detail",
    ),
]
