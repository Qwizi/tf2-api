"""Module contains the views for the colors app."""
from django_filters import rest_framework as filters
from rest_framework import generics

from colors.models import Color
from colors.serializers import ColorSerializer


class ColorList(generics.ListAPIView):
    """List all colors."""

    queryset = Color.objects.all()
    serializer_class = ColorSerializer
    filter_backends = [filters.DjangoFilterBackend]  # noqa: RUF012

