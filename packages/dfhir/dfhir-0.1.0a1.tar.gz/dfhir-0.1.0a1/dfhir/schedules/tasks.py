"""Schedule tasks."""

from celery import shared_task
from django.utils.timezone import timedelta

from nebula.slots.models import Slot

from .models import Schedule


@shared_task
def create_slots(
    schedule_id,
    slot_duration,
):
    """Schedule task to create slots."""
    schedule = Schedule.objects.prefetch_related(
        "specialty", "service_type", "service_category"
    ).get(id=schedule_id)
    start_time = schedule.start_date_time
    end_time = schedule.end_date_time

    current_time = start_time
    while current_time + timedelta(minutes=slot_duration) <= end_time:
        slot = Slot.objects.create(
            schedule=schedule,
            practitioner=schedule.practitioner,
            start_date_time=current_time,
            end_date_time=current_time + timedelta(minutes=slot_duration),
            # Add any other fields that are necessary
        )
        slot.specialty.add(*schedule.specialty.all())
        slot.service_type.add(*schedule.service_type.all())
        slot.service_category.add(*schedule.service_category.all())

        current_time += timedelta(minutes=slot_duration)
