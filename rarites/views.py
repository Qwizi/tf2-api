"""Module contains the views for the rarities app."""
from django_filters import rest_framework as filters
from rest_framework import generics

from rarites.models import Rarity
from rarites.serializers import RaritySerializer


class RarityList(generics.ListAPIView):
    """List all rarities."""

    queryset = Rarity.objects.all()
    serializer_class = RaritySerializer
    filter_backends = [filters.DjangoFilterBackend]    # noqa: RUF012
