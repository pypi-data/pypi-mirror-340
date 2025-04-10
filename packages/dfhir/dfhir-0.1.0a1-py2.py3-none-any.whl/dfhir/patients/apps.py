"""Patients app configuration."""

import contextlib

from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class PatientsConfig(AppConfig):
    """Patients app configuration."""

    default_auto_field = "django.db.models.BigAutoField"
    name = "nebula.patients"
    verbose_name = _("Patients")

    def ready(self):
        """Import signals."""
        with contextlib.suppress(ImportError):
            import nebula.patients.signals  # noqa: F401
