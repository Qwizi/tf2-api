"""Serializers for the maps app."""
from rest_framework import serializers

from maps.models import Map


class MapSerializer(serializers.ModelSerializer):
    """Serializer for the Color model."""

    class Meta:
        """Meta class for the ColorSerializer."""

        model = Map
        fields = ("id", "game_item_id", "name", "localizedname", "authors")
