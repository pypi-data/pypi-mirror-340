"""User role choices."""

from django.db import models
from django.utils.translation import gettext_lazy as _


class UserRoleChoices(models.TextChoices):
    """User role choices."""

    PATIENT = "patient", _("patient")
    PRACTITIONER = "practitioner", _("practitioner")
    ADMIN = "admin", _("admin")
