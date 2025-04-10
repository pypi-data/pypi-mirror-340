"""EPisode of Care app configuration."""

from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class EpisodeofcareConfig(AppConfig):
    """Episode of Care app configuration."""

    default_auto_field = "django.db.models.BigAutoField"
    name = "nebula.episodeofcare"
    verbose_name = _("Episode of Care")
