"""Appointment serializers."""

from rest_framework import serializers

from nebula.users.serializers import UserSerializer

from .models import Admin


class AdminWithoutOrganizationSerializer(serializers.ModelSerializer):
    """Admin serializer without the organization."""

    email = serializers.EmailField(write_only=True)
    username = serializers.CharField(required=False, write_only=True)
    password = serializers.CharField(required=True, write_only=True)
    user = UserSerializer(many=False, read_only=True)

    class Meta:
        """Meta class."""

        model = Admin
        exclude = ["created_at", "updated_at", "organization"]

    def create(self, validated_data):
        """Create an Admin instance."""
        email = validated_data.pop("email")
        username = validated_data.pop("username", None)
        password = validated_data.pop("password")

        user_data = {
            "email": email,
            "username": username,
            "password": password,
            "role": [{"display": "admin"}],
        }

        user_serializer = UserSerializer(data=user_data)
        user_serializer.is_valid(raise_exception=True)
        user = user_serializer.save()

        validated_data["user"] = user

        return super().create(validated_data)


class AdminSerializer(AdminWithoutOrganizationSerializer):
    """Appointment serializer."""

    class Meta:
        """Meta class."""

        model = Admin
        exclude = ["created_at", "updated_at"]
