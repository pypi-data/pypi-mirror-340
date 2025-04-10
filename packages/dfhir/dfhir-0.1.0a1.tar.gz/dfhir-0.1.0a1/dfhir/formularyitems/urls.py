"""formulary item urls."""

from django.urls import path

from nebula.formularyitems import views

app_name = "formularyitems"

urlpatterns = [
    path(
        "formularyitems/",
        views.FormularyItemListView.as_view(),
        name="formularyitem-list",
    ),
    path(
        "formularyitems/<int:pk>/",
        views.FormularyItemDetailView.as_view(),
        name="formularyitem-detail",
    ),
]
