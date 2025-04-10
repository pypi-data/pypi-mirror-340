"""charge item urls."""

from django.urls import path

from nebula.chargeitems import views

app_name = "chargeitems"

urlpatterns = [
    path("chargeitems/", views.ChargeItemListView.as_view()),
    path("chargeitems/<int:pk>/", views.ChargeItemDetailView.as_view()),
]
