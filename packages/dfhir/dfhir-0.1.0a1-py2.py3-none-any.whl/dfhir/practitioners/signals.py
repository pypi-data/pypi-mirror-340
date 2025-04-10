"""Practitioner signals."""

from django.db import transaction
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.http import HttpRequest

from nebula.users.models import Invite

from .models import PractitionerExt


@receiver(post_save, sender=PractitionerExt)
def send_practitioner_email(sender, instance, created, **kwargs):
    """Send practitioner email."""
    if created and not (
        Invite.objects.filter(email__iexact=instance.email, practitioner=instance)
        .order_by("created_at")
        .last()
    ):
        invitation = Invite.create(email=instance.email, practitioner=instance)

        request = HttpRequest()
        request.META["HTTP_HOST"] = "localhost:3000"
        request.META["SERVER_NAME"] = "localhost"
        request.META["SERVER_PORT"] = "3000"

        transaction.on_commit(
            lambda: {
                invitation.send_invitation(
                    request,
                    first_name=instance.name.last().family,
                    last_name=" ".join(instance.name.last().given),
                )
            }
        )
