"""Patient views."""

from django.http import Http404
from drf_spectacular.utils import extend_schema
from rest_framework import status
from rest_framework.exceptions import ValidationError
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from nebula.users.models import Invite
from nebula.users.serializers import UserSerializer

from .models import Patient
from .serializers import PatientSerializer


class PatientUserCreateView(APIView):
    """Create a patient user."""

    permission_classes = [AllowAny]

    @extend_schema(request=PatientSerializer, responses={201: UserSerializer})
    def post(self, request):
        """Create a patient user."""
        request_data = request.data
        request_data["role"] = [{"display": "patient"}]

        if "token" not in request_data:
            raise ValidationError(detail="Token not present")

        token = request_data.pop("token")
        serializer = UserSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        if token:
            try:
                invitation = Invite.objects.get(
                    key=token, patient__isnull=False, practitioner__isnull=True
                )
            except Invite.DoesNotExist as err:
                raise ValidationError(
                    {"error": "Invitation token does not exist"}
                ) from err
            invitation.validate_and_accept_invite()
            patient = invitation.patient
            serializer.save()
            patient.update_user(serializer.data["id"])
        else:
            # TODO: Should we allow creation without a token?
            serializer.save()

        return Response(serializer.data, status=status.HTTP_201_CREATED)


class PatientListView(APIView):
    """Patient list view."""

    permission_classes = [AllowAny]

    @extend_schema(responses={200: PatientSerializer(many=True)})
    def get(self, request, pk=None):
        """Get all patients."""
        queryset = Patient.objects.all()
        serializer = PatientSerializer(queryset, many=True)
        return Response(serializer.data)

    @extend_schema(request=PatientSerializer, responses={200: PatientSerializer})
    def post(self, request):
        """Create a patient."""
        request_data = request.data
        request_data.pop("user", None)

        serializer = PatientSerializer(data=request_data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)


class PatientDetailView(APIView):
    """Patient detail view."""

    permission_classes = [AllowAny]

    def get_object(self, pk):
        """Get patient object."""
        try:
            return Patient.objects.get(pk=pk)
        except Patient.DoesNotExist as err:
            raise Http404 from err

    @extend_schema(responses={200: PatientSerializer})
    def get(self, request, pk=None):
        """Get a patient."""
        queryset = self.get_object(pk)
        serializer = PatientSerializer(queryset)
        return Response(serializer.data)

    @extend_schema(responses={200: PatientSerializer})
    def patch(self, request, pk=None):
        """Update a patient."""
        queryset = self.get_object(pk)
        serializer = PatientSerializer(queryset, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

    def delete(self, request, pk=None):
        """Delete a patient."""
        patient = self.get_object(pk)
        patient.user.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
