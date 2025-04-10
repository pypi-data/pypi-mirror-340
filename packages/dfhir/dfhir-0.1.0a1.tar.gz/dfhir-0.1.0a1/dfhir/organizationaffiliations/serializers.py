"""organization affiliation serializers."""

from nebula.base.serializers import (
    BaseWritableNestedModelSerializer,
    CodeableConceptSerializer,
    ExtendedContactDetailSerializer,
    IdentifierSerializer,
    PeriodSerializer,
)
from nebula.endpoints.serializers import EndpointReferenceSerializer
from nebula.healthcareservices.serializers import HealthCareServiceReferenceSerializer
from nebula.locations.serializers import LocationReferenceSerializer
from nebula.organizationaffiliations.models import OrganizationAffiliation
from nebula.organizations.serializers import OrganizationReferenceSerializer


class OrganizationAffiliationSerializer(BaseWritableNestedModelSerializer):
    """organization affiliation serializer."""

    identifier = IdentifierSerializer(many=True, required=False)
    period = PeriodSerializer(required=False, many=False)
    organization = OrganizationReferenceSerializer(required=False, many=False)
    participating_organization = OrganizationReferenceSerializer(
        required=False, many=False
    )
    network = OrganizationReferenceSerializer(required=False, many=True)
    code = CodeableConceptSerializer(required=False, many=True)
    specialty = CodeableConceptSerializer(required=False, many=True)
    location = LocationReferenceSerializer(required=False, many=True)
    healthcare_service = HealthCareServiceReferenceSerializer(required=False, many=True)
    contact = ExtendedContactDetailSerializer(required=False, many=True)
    endpoint = EndpointReferenceSerializer(required=False, many=True)

    class Meta:
        """meta options."""

        model = OrganizationAffiliation
        exclude = ["created_at", "updated_at"]
