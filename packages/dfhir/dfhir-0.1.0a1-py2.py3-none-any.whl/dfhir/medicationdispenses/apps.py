"""medication dispenses app."""

from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class MedicationdispensesConfig(AppConfig):
    """Medication Dispenses Config."""

    default_auto_field = "django.db.models.BigAutoField"
    name = "nebula.medicationdispenses"
    verbose_name = _("Medication Dispenses")
