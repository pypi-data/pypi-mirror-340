"""Plandefinitions app configuration."""

from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class PlandefinitionsConfig(AppConfig):
    """Plandefinitions app configuration."""

    default_auto_field = "django.db.models.BigAutoField"
    name = "nebula.plandefinitions"
    verbose_name = _("Plan definitions")
