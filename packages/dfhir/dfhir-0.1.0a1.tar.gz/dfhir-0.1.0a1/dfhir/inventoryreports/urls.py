"""inventory report urls."""

from django.urls import path

from nebula.inventoryreports import views

app_name = "inventoryreports"

urlpatterns = [
    path(
        "inventoryreports/",
        views.InventoryReportListView.as_view(),
        name="inventoryreport-list",
    ),
    path(
        "api/inventoryreports/<int:pk>/",
        views.InventoryReportDetailView.as_view(),
        name="inventoryreport-list",
    ),
]
