"""medication administration urls."""

from drf_writable_nested.serializers import WritableNestedModelSerializer

from nebula.base.serializers import (
    AnnotationSerializer,
    BaseReferenceModelSerializer,
    BaseWritableNestedModelSerializer,
    CodeableConceptSerializer,
    IdentifierSerializer,
    PeriodSerializer,
    QuantitySerializer,
    RatioSerializer,
    ReferenceSerializer,
    TimingSerializer,
)
from nebula.careplans.serializers import CarePlanReferenceSerializer
from nebula.devices.serializers import DeviceCodeableReferenceSerializer
from nebula.encounters.serializers import EncounterReferenceSerializer
from nebula.medicationadministrations.models import (
    MedicationAdministration,
    MedicationAdministrationDosage,
    MedicationAdministrationPartOf,
    MedicationAdministrationPerformer,
    MedicationAdministrationPerformerActorCodeableReference,
    MedicationAdministrationPerformerActorReference,
    MedicationAdministrationReasonCodeableReference,
    MedicationAdministrationReasonReference,
)
from nebula.medicationrequests.serializers import MedicationRequestReferenceSerializer
from nebula.medications.serializers import MedicationCodeableReferenceSerializer
from nebula.patients.serializers import PatientGroupReferenceSerializer
from nebula.provenances.serializers import ProvenanceReferenceSerializer


class MedicationAdministrationPartOfSerializer(BaseReferenceModelSerializer):
    """medication administration part of serializer."""

    identifier = IdentifierSerializer(many=False, required=False)

    class Meta:
        """Meta."""

        model = MedicationAdministrationPartOf
        exclude = ["created_at", "updated_at"]


class MedicationAdministrationPerformerActorReferenceSerializer(
    BaseReferenceModelSerializer
):
    """medication administration performer actor serializer."""

    identifier = IdentifierSerializer(many=False, required=False)

    class Meta:
        """Meta."""

        model = MedicationAdministrationPerformerActorReference
        exclude = ["created_at", "updated_at"]


class MedicationAdministrationPerformerActorCodeableReferenceSerializer(
    WritableNestedModelSerializer
):
    """medication administration performer actor serializer."""

    concept = CodeableConceptSerializer(many=False, required=False)
    reference = MedicationAdministrationPerformerActorReferenceSerializer(
        many=False, required=False
    )

    class Meta:
        """meta options."""

        model = MedicationAdministrationPerformerActorCodeableReference
        exclude = ["created_at", "updated_at"]


class MedicationAdministrationPerformerSerializer(WritableNestedModelSerializer):
    """medication administration performer serializer."""

    function = CodeableConceptSerializer(many=False, required=False)
    actor = MedicationAdministrationPerformerActorCodeableReferenceSerializer(
        many=False, required=False
    )

    class Meta:
        """Meta."""

        model = MedicationAdministrationPerformer
        exclude = ["created_at", "updated_at"]


class MedicationAdministrationReasonReferenceSerializer(BaseReferenceModelSerializer):
    """medication administration reason reference serializer."""

    identifier = IdentifierSerializer(many=False, required=False)

    class Meta:
        """meta options."""

        model = MedicationAdministrationReasonReference
        exclude = ["created_at", "updated_at"]


class MedicationAdministrationReasonCodeableReferenceSerializer(
    WritableNestedModelSerializer
):
    """medication administration reason codeable reference serializer."""

    concept = CodeableConceptSerializer(many=False, required=False)
    reference = MedicationAdministrationReasonReferenceSerializer(
        many=False, required=False
    )

    class Meta:
        """meta options."""

        model = MedicationAdministrationReasonCodeableReference
        exclude = ["created_at", "updated_at"]


class MedicationAdministrationDosageSerializer(WritableNestedModelSerializer):
    """medication administration dosage serializer."""

    site = CodeableConceptSerializer(many=False, required=False)
    route = CodeableConceptSerializer(many=False, required=False)
    method = CodeableConceptSerializer(many=False, required=False)
    dose = QuantitySerializer(many=False, required=False)
    rate_ratio = RatioSerializer(many=False, required=False)
    rate_quantity = QuantitySerializer(many=False, required=False)

    class Meta:
        """meta options."""

        model = MedicationAdministrationDosage
        exclude = ["created_at", "updated_at"]


class MedicationAdministrationSerializer(BaseWritableNestedModelSerializer):
    """medication administration serializer."""

    identifier = IdentifierSerializer(many=True, required=False)
    based_on = CarePlanReferenceSerializer(many=True, required=False)
    part_of = MedicationAdministrationPartOfSerializer(many=True, required=False)
    status_reason = CodeableConceptSerializer(many=True, required=False)
    category = CodeableConceptSerializer(many=True, required=False)
    medication = MedicationCodeableReferenceSerializer(many=False, required=False)
    subject = PatientGroupReferenceSerializer(many=False, required=False)
    encounter = EncounterReferenceSerializer(many=False, required=False)
    supporting_information = ReferenceSerializer(many=True, required=False)
    occurrence_period = PeriodSerializer(many=False, required=False)
    occurrence_timing = TimingSerializer(many=False, required=False)
    sub_potent_reason = CodeableConceptSerializer(many=True, required=False)
    performer = MedicationAdministrationPerformerSerializer(many=True, required=False)
    reason = MedicationAdministrationReasonCodeableReferenceSerializer(
        many=True, required=False
    )
    request = MedicationRequestReferenceSerializer(many=False, required=False)
    device = DeviceCodeableReferenceSerializer(many=True, required=False)
    note = AnnotationSerializer(many=True, required=False)
    dosage = MedicationAdministrationDosageSerializer(many=False, required=False)
    event_history = ProvenanceReferenceSerializer(many=True, required=False)

    class Meta:
        """meta options."""

        model = MedicationAdministration
        exclude = ["created_at", "updated_at"]
