"""Authentication views for the Nebula app."""

from abc import ABC, abstractmethod

from dj_rest_auth.views import LoginView
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken

from nebula.admins.models import Admin
from nebula.admins.serializers import AdminSerializer
from nebula.patients.models import Patient
from nebula.patients.serializers import PatientSerializer
from nebula.practitioners.models import Practitioner
from nebula.practitioners.serializers import (
    PractitionerSerializerWithUserDetail,
)
from nebula.users.models import Role

from .exceptions import AuthenticationError


class LoginBaseClass(ABC, LoginView):
    """This class inherits the LoginView from the rest_auth package.
    Django rest auth lib does not support the refresh token
    logic. However,restframework_simplejwt does. Rest auth was
    used because it's based off all-auth which can be used for
    social logins as well as signing in with either username or
    password(of which simplejwt does not support). The two libraries
    were combined to give the required results.
    """

    def get_extra_payload(self) -> dict:
        """This method is used to add extra payload to the refresh token."""
        return {}

    def get_token(self, user):
        """Generate the refresh token."""
        refresh_token = RefreshToken.for_user(user)
        for key, value in self.get_extra_payload().items():
            refresh_token[key] = value
        return refresh_token

    @abstractmethod
    def login(self):
        """Login in the user."""
        pass

    def get_response(self):
        """Return the response with the refresh token."""
        data = {}

        refresh = self.get_token(self.user)
        # generate access and refresh tokens
        data["refresh"] = str(refresh)
        data["access"] = str(refresh.access_token)

        return Response(data)


class PractitionerLoginView(LoginBaseClass):
    """Login view for practitioners."""

    def login(self):
        """Login the practitioner."""
        try:
            self.user = self.serializer.validated_data["user"]
            # check if user has practitioner among its roles
            self.user.role.get(display="practitioner")
            return self.user
        except Role.DoesNotExist as err:
            raise AuthenticationError from err

    def get_extra_payload(self) -> dict:
        """Return the practitioner data."""
        practitioner = Practitioner.objects.get(user=self.user)
        serializer = PractitionerSerializerWithUserDetail(practitioner)
        return {"practitioner": serializer.data}


class PatientLoginView(LoginBaseClass):
    """Login view for patients."""

    def login(self):
        """Login the patient."""
        try:
            self.user = self.serializer.validated_data["user"]
            self.user.role.get(display="patient")
            return self.user
        except Role.DoesNotExist as err:
            raise AuthenticationError from err

    def get_extra_payload(self) -> dict:
        """Return the patient data."""
        practitioner = Patient.objects.get(user=self.user)
        serializer = PatientSerializer(practitioner)
        return {"patient": serializer.data}


class AdminLoginView(LoginBaseClass):
    """Login view for admins."""

    def login(self):
        """Login the admin."""
        try:
            self.user = self.serializer.validated_data["user"]
            self.user.role.get(display="admin")
            return self.user
        except Role.DoesNotExist as err:
            raise AuthenticationError from err

    def get_extra_payload(self) -> dict:
        """Return the admin data."""
        admin = Admin.objects.get(user=self.user)
        serializer = AdminSerializer(admin)
        return {"admin": serializer.data}
