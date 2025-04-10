"""Users app configuration."""

import contextlib

from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class UsersConfig(AppConfig):
    """App configuration."""

    name = "nebula.users"
    verbose_name = _("Users")

    def ready(self):
        """Import signals."""
        with contextlib.suppress(ImportError):
            import nebula.users.signals  # noqa: F401
