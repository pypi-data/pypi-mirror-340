"""molecular definitions URL Configuration."""

from django.urls import path

from nebula.moleculardefinitions import views

app_name = "moleculardefinitions"


urlpatterns = [
    path("moleculardefinitions/", views.MolecularDefinitionListView.as_view()),
    path(
        "moleculardefinitions/<int:pk>/", views.MolecularDefinitionDetailView.as_view()
    ),
]
