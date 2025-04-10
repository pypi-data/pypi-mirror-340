"""Practitioner views."""

from django.http import Http404
from drf_spectacular.utils import extend_schema
from rest_framework import status
from rest_framework.exceptions import ValidationError
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from nebula.users.models import Invite
from nebula.users.serializers import UserSerializer

from .filters import PractitionerFilter
from .models import (
    Practitioner,
    PractitionerExt,
    PractitionerRole,
    PractitionerRoleCode,
)
from .serializers import (
    PractitionerExtSerializer,
    PractitionerRoleCodeSerializer,
    PractitionerRoleSerializer,
    PractitionerRoleWithPractitionerIdSerializer,
)


class PractitionerUserCreateView(APIView):
    """Practitioner user create view."""

    permission_classes = [AllowAny]

    @extend_schema(request=PractitionerExtSerializer, responses={201: UserSerializer})
    def post(self, request):
        """Create a practitioner user."""
        request_data = request.data
        request_data["role"] = [{"display": "practitioner"}]

        if "token" not in request_data:
            raise ValidationError(detail="Token not present")

        token = request_data.pop("token")
        serializer = UserSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        if token:
            try:
                invitation = Invite.objects.get(
                    key=token, practitioner__isnull=False, patient__isnull=True
                )
            except Invite.DoesNotExist as err:
                raise ValidationError(
                    {"error": "Invitation token does not exist"}
                ) from err
            invitation.validate_and_accept_invite()
            practitioner = invitation.practitioner
            serializer.save()
            practitioner.update_user(serializer.data["id"])
        else:
            # TODO: Should we allow creation without a token?
            return Response(
                ValidationError("Token not present"), status=status.HTTP_400_BAD_REQUEST
            )

        return Response(serializer.data, status=status.HTTP_201_CREATED)


class PractitionerListView(APIView):
    """Practitioner list view."""

    permission_classes = [AllowAny]

    @extend_schema(responses={200: PractitionerExtSerializer(many=True)})
    def get(self, request, pk=None):
        """Get practitioners."""
        queryset = PractitionerExt.objects.all()
        practitioners_filter = PractitionerFilter(request.GET, queryset=queryset)
        serializer = PractitionerExtSerializer(practitioners_filter.qs, many=True)
        return Response(serializer.data)

    @extend_schema(
        request=PractitionerExtSerializer, responses={200: PractitionerExtSerializer}
    )
    def post(self, request):
        """Create a practitioner."""
        request_data = request.data
        request_data.pop("user", None)

        serializer = PractitionerExtSerializer(data=request_data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)


class PractitionerDetailView(APIView):
    """Practitioner detail view."""

    permission_classes = [AllowAny]

    def get_object(self, pk):
        """Get practitioner object."""
        try:
            return PractitionerExt.objects.get(pk=pk)
        except Practitioner.DoesNotExist as err:
            raise Http404 from err

    @extend_schema(responses={200: PractitionerExtSerializer})
    def get(self, request, pk=None):
        """Get a practitioner."""
        queryset = self.get_object(pk)
        serializer = PractitionerExtSerializer(queryset)
        return Response(serializer.data)

    @extend_schema(responses={200: PractitionerExtSerializer})
    def patch(self, request, pk=None):
        """Update a practitioner."""
        queryset = self.get_object(pk)
        serializer = PractitionerExtSerializer(
            queryset, data=request.data, partial=True
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

    def delete(self, request, pk=None):
        """Delete a practitioner."""
        practitioner = self.get_object(pk)
        practitioner.user.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class PractitionerRoleListView(APIView):
    """Practitioner role list view."""

    permission_classes = [AllowAny]

    @extend_schema(responses={200: PractitionerRoleWithPractitionerIdSerializer})
    def get(self, request, pk=None):
        """Get practitioner roles."""
        queryset = PractitionerRole.objects.all()
        serializer = PractitionerRoleSerializer(queryset, many=True)
        return Response(serializer.data)

    @extend_schema(
        request=PractitionerRoleSerializer,
        responses={200: PractitionerRoleWithPractitionerIdSerializer},
    )
    def post(self, request):
        """Create a practitioner role."""
        request_data = request.data
        serializer = PractitionerRoleSerializer(data=request_data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)


class PractitionerRoleDetailView(APIView):
    """Practitioner role detail view."""

    def get_object(self, pk):
        """Get practitioner role object."""
        try:
            return PractitionerRole.objects.get(pk=pk)
        except PractitionerRole.DoesNotExist as err:
            raise Http404 from err

    @extend_schema(responses={200: PractitionerRoleWithPractitionerIdSerializer})
    def get(self, request, pk=None):
        """Get a practitioner role."""
        queryset = self.get_object(pk)
        serializer = PractitionerRoleSerializer(queryset)
        return Response(serializer.data)

    @extend_schema(responses={200: PractitionerRoleWithPractitionerIdSerializer})
    def patch(self, request, pk=None):
        """Update a practitioner role."""
        queryset = self.get_object(pk)
        serializer = PractitionerRoleSerializer(
            queryset, data=request.data, partial=True
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

    def delete(self, request, pk=None):
        """Delete a practitioner role."""
        practitioner_role = self.get_object(pk)
        practitioner_role.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class PractitionerRoleCodeListView(APIView):
    """Practitioner role code list view."""

    permission_classes = [AllowAny]

    @extend_schema(responses={200: PractitionerRoleCodeSerializer})
    def get(self, request, pk=None):
        """Get practitioner role codes."""
        queryset = PractitionerRoleCode.objects.all()
        serializer = PractitionerRoleCodeSerializer(queryset, many=True)
        return Response(serializer.data)
