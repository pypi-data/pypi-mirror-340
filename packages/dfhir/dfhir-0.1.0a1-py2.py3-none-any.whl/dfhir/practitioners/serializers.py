"""Practitioner serializers."""

from rest_framework import serializers

from nebula.base.serializers import (
    AddressSerializer,
    AttachmentSerializer,
    AvailabilitySerializer,
    BaseReferenceModelSerializer,
    BaseWritableNestedModelSerializer,
    CodeableConceptSerializer,
    CommunicationSerializer,
    ContactPointSerializer,
    ExtendedContactDetailSerializer,
    HumanNameSerializer,
    IdentifierSerializer,
    OrganizationReferenceSerializer,
    PeriodSerializer,
    QualificationSerializer,
)
from nebula.endpoints.serializers import EndpointReferenceSerializer
from nebula.healthcareservices.serializers import HealthCareServiceReferenceSerializer
from nebula.locations.serializers import LocationReferenceSerializer
from nebula.users.serializers import UserSerializer

from .models import (
    Practitioner,
    PractitionerExt,
    PractitionerPractitionerRoleReference,
    PractitionerReference,
    PractitionerRole,
    PractitionerRoleCode,
    PractitionerRoleReference,
)


class PractitionerReferenceSerializer(BaseReferenceModelSerializer):
    """Practitioner reference serializer."""

    identifier = IdentifierSerializer(many=False, required=False)

    class Meta:
        """Meta class."""

        model = PractitionerReference
        exclude = ["created_at", "updated_at"]


class PractitionerRoleCodeSerializer(serializers.ModelSerializer):
    """Practitioner Role Code serializer."""

    class Meta:
        """Meta class."""

        model = PractitionerRoleCode
        exclude = ["created_at", "updated_at"]


# Practitioner role
class PractitionerRoleSerializer(BaseWritableNestedModelSerializer):
    """Practitioner Role serializer."""

    identifier = IdentifierSerializer(many=True, required=False)
    period = PeriodSerializer(many=False, required=False)
    practitioner = PractitionerReferenceSerializer(many=False, required=False)
    organization = OrganizationReferenceSerializer(many=False, required=False)
    network = OrganizationReferenceSerializer(many=True, required=False)
    code = CodeableConceptSerializer(many=True, required=False)
    specialty = CodeableConceptSerializer(many=True, required=False)
    location = LocationReferenceSerializer(many=True, required=False)
    healthcare_service = HealthCareServiceReferenceSerializer(many=True, required=False)
    characteristic = CodeableConceptSerializer(many=True, required=False)
    availability = AvailabilitySerializer(many=False, required=False)
    communication = CodeableConceptSerializer(many=True, required=False)
    contact = ExtendedContactDetailSerializer(many=True, required=False)
    endpoint = EndpointReferenceSerializer(many=True, required=False)

    class Meta:
        """Meta class."""

        model = PractitionerRole
        exclude = ["created_at", "updated_at"]


class PractitionerRoleWithPractitionerIdSerializer(PractitionerRoleSerializer):
    """Practitioner Role with Practitioner ID serializer."""

    class Meta:
        """Meta class."""

        model = PractitionerRole
        exclude = ["created_at", "updated_at"]


class PractitionerSerializer(BaseWritableNestedModelSerializer):
    """Practitioner serializer."""

    identifier = IdentifierSerializer(many=True, required=False)
    name = HumanNameSerializer(many=True, required=False)
    telecom = ContactPointSerializer(many=True, required=False)
    photo = AttachmentSerializer(many=True, required=False)
    communication = CommunicationSerializer(many=True, required=False)
    qualification = QualificationSerializer(many=True, required=False)
    address = AddressSerializer(many=True, required=False)

    class Meta:
        """Meta class."""

        model = Practitioner
        exclude = ["created_at", "updated_at"]


class PractitionerExtSerializer(PractitionerSerializer):
    """Practitioner serializer with user detail."""

    class Meta:
        """Meta class."""

        model = PractitionerExt
        exclude = ["created_at", "updated_at"]


class PractitionerSerializerWithUserDetail(PractitionerSerializer):
    """Practitioner serializer with user detail."""

    user = UserSerializer()

    class Meta:
        """Meta class."""

        model = Practitioner
        exclude = ["created_at", "updated_at"]


class PractitionerPractitionerRoleReferenceSerializer(BaseReferenceModelSerializer):
    """Practitioner Practitioner Role reference serializer."""

    identifier = IdentifierSerializer(many=False, required=False)

    class Meta:
        """Meta class."""

        model = PractitionerPractitionerRoleReference
        exclude = ["created_at", "updated_at"]


class PractitionerRoleReferenceSerializer(BaseReferenceModelSerializer):
    """Practitioner Role reference serializer."""

    identifier = IdentifierSerializer(many=False, required=False)

    class Meta:
        """Meta class."""

        model = PractitionerRoleReference
        exclude = ["created_at", "updated_at"]
