"""Devicedispenses app configuration."""

from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class DevicedispensesConfig(AppConfig):
    """Devicedispenses app configuration."""

    default_auto_field = "django.db.models.BigAutoField"
    name = "nebula.devicedispenses"
    verbose_name = _("device dispenses")
