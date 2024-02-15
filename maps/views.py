"""Views for the maps app."""
from django_filters import rest_framework as filters
from rest_framework import generics

from maps.models import Map
from maps.serializers import MapSerializer


# Create your views here.
class MapList(generics.ListAPIView):
    """List all maps."""

    queryset = Map.objects.all()
    serializer_class = MapSerializer
    filter_backends = [filters.DjangoFilterBackend]  # noqa: RUF012
