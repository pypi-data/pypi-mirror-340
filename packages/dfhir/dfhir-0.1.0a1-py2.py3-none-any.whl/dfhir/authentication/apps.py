"""Authentication app configuration."""

from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class AuthenticationConfig(AppConfig):
    """App configuration."""

    default_auto_field = "django.db.models.BigAutoField"
    name = "nebula.authentication"
    verbose_name = _("Authentication")
