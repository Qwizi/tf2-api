"""Views for the qualities app."""

from django_filters import rest_framework as filters
from rest_framework import generics

from qualities.models import Quality
from qualities.serializers import QualitySerializer


class QualityList(generics.ListAPIView):
    """List all qualities."""

    queryset = Quality.objects.all()
    serializer_class = QualitySerializer
    filter_backends = [filters.DjangoFilterBackend]  # noqa: RUF012

