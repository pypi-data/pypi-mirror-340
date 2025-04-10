"""Admin models."""

from django.contrib.auth import get_user_model
from django.db import models
from django.utils.translation import gettext_lazy as _

from nebula.base.models import TimeStampedModel


class Admin(TimeStampedModel):
    """Admin model."""

    user = models.ForeignKey(
        get_user_model(), on_delete=models.SET_NULL, related_name="admins", null=True
    )
    first_name = models.CharField(max_length=255, blank=True, null=True)
    last_name = models.CharField(max_length=255, blank=True, null=True)
    date_of_birth = models.DateField(null=True, blank=True)
    email = models.EmailField(_("email address"), null=True)
    active = models.BooleanField(default=True)
    organization = models.ForeignKey(
        "organizations.organization",
        on_delete=models.DO_NOTHING,
        null=True,
        blank=True,
        related_name="admin_organization",
    )
