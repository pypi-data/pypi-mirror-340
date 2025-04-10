"""transport app."""

from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class TransportsConfig(AppConfig):
    """Transport app config."""

    default_auto_field = "django.db.models.BigAutoField"
    name = "nebula.transports"
    verbose_name = _("Transports")
