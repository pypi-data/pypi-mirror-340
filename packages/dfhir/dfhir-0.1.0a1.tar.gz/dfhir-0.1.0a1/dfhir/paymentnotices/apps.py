"""Payment Notices App Configuration."""

from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class PaymentnoticesConfig(AppConfig):
    """Payment Notices App Configuration."""

    default_auto_field = "django.db.models.BigAutoField"
    name = "nebula.paymentnotices"
    verbose_name = _("Payment Notices")
