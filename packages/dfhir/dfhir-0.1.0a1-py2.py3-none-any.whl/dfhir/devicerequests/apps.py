"""Devicerequests app configuration."""

from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class DevicerequestsConfig(AppConfig):
    """Devicerequests app configuration."""

    default_auto_field = "django.db.models.BigAutoField"
    name = "nebula.devicerequests"
    verbose_name = _("devicerequests")
