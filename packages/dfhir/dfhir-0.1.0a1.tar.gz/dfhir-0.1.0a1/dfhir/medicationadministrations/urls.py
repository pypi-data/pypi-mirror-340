"""medication administrations urls."""

from django.urls import path

from nebula.medicationadministrations.views import (
    MedicationAdministrationDetailView,
    MedicationAdministrationListView,
)

app_name = "medicationadministrations"

urlpatterns = [
    path(
        "medicationadministrations/",
        MedicationAdministrationListView.as_view(),
        name="medicationadministration-list",
    ),
    path(
        "medicationadministrations/<int:pk>/",
        MedicationAdministrationDetailView.as_view(),
        name="medicationadministration-detail",
    ),
]
