"""Schedule signals module."""

from django.db.models.signals import post_save
from django.dispatch import receiver

from .models import Schedule
from .tasks import create_slots


@receiver(post_save, sender=Schedule)
def create_schedule_slots(sender, instance, created, **kwargs):
    """Create schedule slots."""
    if created:
        # Trigger the asynchronous task to create slots
        create_slots.delay(instance.id, instance.slots_duration)
