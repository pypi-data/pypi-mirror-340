"""Vision prescription app configuration."""

from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class VisionprescriptionsConfig(AppConfig):
    """Vision prescriptions app configuration."""

    default_auto_field = "django.db.models.BigAutoField"
    name = "nebula.visionprescriptions"
    verbose_name = _("Vision Prescriptions")
