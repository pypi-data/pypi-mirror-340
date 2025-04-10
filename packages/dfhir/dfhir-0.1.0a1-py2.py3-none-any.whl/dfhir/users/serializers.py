"""User serializers."""

from drf_writable_nested.serializers import WritableNestedModelSerializer
from rest_framework import serializers

from nebula.users.models import Role, User


class UserRoleSerializer(serializers.ModelSerializer):
    """User role serializer."""

    class Meta:
        """Meta class."""

        model = Role
        fields = ["id", "display"]


class UserSerializer(WritableNestedModelSerializer):
    """User serializer."""

    role = UserRoleSerializer(many=True)

    class Meta:
        """Meta class."""

        model = User
        fields = [
            "id",
            "email",
            "username",
            "role",
            "password",
        ]
        extra_kwargs = {"password": {"write_only": True}}
