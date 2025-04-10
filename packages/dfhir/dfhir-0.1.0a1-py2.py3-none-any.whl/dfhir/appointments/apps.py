"""Appointments app configuration."""

from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class AppointmentsConfig(AppConfig):
    """Appointments app configuration."""

    default_auto_field = "django.db.models.BigAutoField"
    name = "nebula.appointments"
    verbose_name = _("Appointments")
