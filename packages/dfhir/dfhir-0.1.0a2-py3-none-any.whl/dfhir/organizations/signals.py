"""Signals for the organizations app."""

from django.db.models.signals import post_save
from django.dispatch import receiver

from .models import Organization


@receiver(post_save, sender=Organization)
def update_admin_organization(sender, instance, **kwargs):
    """Update the organization field in the admin object."""
    if instance.admin:
        admin = instance.admin
        admin.organization = instance
        admin.save()
