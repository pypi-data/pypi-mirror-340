"""Admin app config."""

from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class AdminsConfig(AppConfig):
    """Admin config."""

    default_auto_field = "django.db.models.BigAutoField"
    name = "dfhir.admins"
    verbose_name = _("Admins")
