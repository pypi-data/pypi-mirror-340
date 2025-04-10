"""Practitioner filters."""

from django_filters import rest_framework as filters

from nebula.practitioners.models import PractitionerExt


class PractitionerFilter(filters.FilterSet):
    """Practitioner filter."""

    user = filters.CharFilter(field_name="user")

    class Meta:
        """Meta class."""

        model = PractitionerExt
        fields = ["gender", "active"]
