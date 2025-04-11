"""Views for admin."""

from django.http import Http404
from drf_spectacular.utils import extend_schema
from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Admin
from .serializers import AdminSerializer


class AdminListView(APIView):
    """Admin list view."""

    permission_classes = [AllowAny]

    @extend_schema(responses={200: AdminSerializer(many=True)})
    def get(self, request, pk=None):
        """Get all admins."""
        queryset = Admin.objects.all()
        serializer = AdminSerializer(queryset, many=True)
        return Response(serializer.data)

    @extend_schema(request=AdminSerializer, responses={200: AdminSerializer})
    def post(self, request):
        """Create a admin."""
        request_data = request.data
        request_data.pop("user", None)

        serializer = AdminSerializer(data=request_data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)


class AdminDetailView(APIView):
    """Admin detail view."""

    permission_classes = [AllowAny]

    def get_object(self, pk):
        """Get admin object."""
        try:
            return Admin.objects.get(pk=pk)
        except Admin.DoesNotExist as err:
            raise Http404 from err

    @extend_schema(responses={200: AdminSerializer})
    def get(self, request, pk=None):
        """Get a admin."""
        queryset = self.get_object(pk)
        serializer = AdminSerializer(queryset)
        return Response(serializer.data)

    @extend_schema(responses={200: AdminSerializer})
    def patch(self, request, pk=None):
        """Update a admin."""
        queryset = self.get_object(pk)
        serializer = AdminSerializer(queryset, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

    def delete(self, request, pk=None):
        """Delete a admin."""
        admin = self.get_object(pk)
        admin.user.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
