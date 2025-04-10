"""Device definition app config."""

from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class DevicedefinitionsConfig(AppConfig):
    """Device Definition config."""

    default_auto_field = "django.db.models.BigAutoField"
    name = "nebula.devicedefinitions"
    verbose_name = _("Device Definitions")
