"""User models for nebula."""

import datetime
from typing import ClassVar

from django.conf import settings
from django.contrib.auth.models import AbstractBaseUser
from django.core.mail import send_mail
from django.db import models
from django.http import HttpResponse
from django.template.loader import render_to_string
from django.urls import reverse
from django.utils import timezone
from django.utils.crypto import get_random_string
from django.utils.html import strip_tags
from django.utils.translation import gettext_lazy as _
from rest_framework.exceptions import ValidationError

from nebula.base.models import PHONE_REGEX, TimeStampedModel

from .choices import UserRoleChoices
from .managers import BaseInvitationManager, UserManager


class User(AbstractBaseUser, TimeStampedModel):
    """Default custom user model for nebula.
    If adding fields that need to be filled at user signup,
    check forms.SignupForm and forms.SocialSignupForms accordingly.
    """

    email = models.EmailField(_("email address"), unique=True, null=True)
    username = models.CharField(
        _("Phone number of the User"),
        unique=True,
        validators=[PHONE_REGEX],
        max_length=17,
        null=True,
    )
    role = models.ManyToManyField("Role", related_name="user_role")

    USERNAME_FIELD = "username"
    REQUIRED_FIELDS = []

    objects: ClassVar[UserManager] = UserManager()

    def get_absolute_url(self) -> str:
        """Get URL for user's detail view.

        Returns:
            str: URL for user detail.

        """
        return reverse("users:detail", kwargs={"pk": self.id})


class Role(TimeStampedModel):
    """Role model for nebula."""

    display = models.CharField(max_length=50, choices=UserRoleChoices.choices)


class AbstractBaseInvitation(models.Model):
    """Abstract base invitation model."""

    accepted = models.BooleanField(verbose_name=_("accepted"), default=False)
    key = models.CharField(verbose_name=_("key"), max_length=64, unique=True)
    sent = models.DateTimeField(verbose_name=_("sent"), null=True)
    inviter = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        verbose_name=_("inviter"),
        null=True,
        blank=True,
        on_delete=models.CASCADE,
    )

    objects = BaseInvitationManager()

    class Meta:
        """Meta options for AbstractBaseInvitation."""

        abstract = True

    @classmethod
    def create(cls, email, inviter=None, **kwargs):
        """Create an invitation."""
        raise NotImplementedError("You should implement the create method class")

    def key_expired(self):
        """Check if the key has expired."""
        raise NotImplementedError("You should implement the key_expired method")

    def send_invitation(self, request, **kwargs):
        """Send the invitation."""
        raise NotImplementedError("You should implement the send_invitation method")

    def __str__(self):
        """Return the string representation of the invitation."""
        raise NotImplementedError("You should implement the __str__ method")


class Invite(TimeStampedModel, AbstractBaseInvitation):
    """Invite model for nebula."""

    practitioner = models.ForeignKey(
        "practitioners.PractitionerExt",
        on_delete=models.DO_NOTHING,
        related_name="practitioner_invite",
        null=True,
    )
    patient = models.ForeignKey(
        "patients.Patient",
        on_delete=models.DO_NOTHING,
        related_name="patient_invite",
        null=True,
    )
    email = models.EmailField(
        unique=True,
        verbose_name=_("e-mail address"),
        max_length=settings.EMAIL_MAX_LENGTH,
    )

    def __str__(self):
        """Return the string representation of the invitation."""
        return f"Invite for {self.practitioner.email if self.practitioner else self.patient.email} - Token: {self.token}"

    @classmethod
    def create(cls, email, inviter=None, **kwargs):
        """Create an invitation."""
        key = get_random_string(64).lower()
        instance = cls._default_manager.create(
            email=email, key=key, inviter=inviter, **kwargs
        )
        return instance

    def key_expired(self):
        """Check if the key has expired."""
        expiration_date = self.sent + datetime.timedelta(
            days=settings.INVITATION_EXPIRY,
        )
        return expiration_date <= timezone.now()

    def send_invitation(self, request, **kwargs):
        """Send the invitation."""
        organization_name = "Test Hospital"

        subject = f"You’re Invited to Join {organization_name} on CareFusion365"
        context = {
            "first_name": kwargs.get("first_name"),
            "last_name": kwargs.get("last_name"),
            "email": self.email,
            "token": self.key,
            "organization_name": organization_name,
        }

        # Render the HTML email template
        html_message = render_to_string("emails/practitioner_welcome.html", context)
        plain_message = strip_tags(html_message)
        from_email = settings.DEFAULT_FROM_EMAIL
        to_email = self.email

        send_mail(
            subject,
            plain_message,
            from_email,
            [to_email],
            html_message=html_message,
        )
        self.sent = datetime.datetime.now()
        self.save()

    def validate_and_accept_invite(self):
        """Validate and accept the invitation."""
        if getattr(settings, "GONE_ON_ACCEPT_ERROR", False) and (
            not self or (self and (self.accepted or self.key_expired()))
        ):
            return HttpResponse(status=410)

        if not self:
            raise ValidationError(
                detail={"error": "Invalid invitation key"},
            )

        if self.accepted:
            raise ValidationError(
                detail={"error": "Invitation already accepted"},
            )

        if self.key_expired():
            raise ValidationError(
                detail={"error": "Invitation key has expired"},
            )
        self.accepted = True
        self.save()
