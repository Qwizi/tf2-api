"""Serializers for the maps app."""
from rest_framework import serializers

from maps.models import Map


class MapSerializer(serializers.ModelSerializer):
    """Serializer for the Color model."""

    def get_dynamic_source(self, obj: Map):
        # Your dynamic logic here to determine the source dynamically
        return obj.get_localized_name()

    def get_authors(self, obj: Map):
        # Your dynamic logic here to determine the source dynamically
        return obj.get_authors()

    localizedname = serializers.SerializerMethodField(method_name="get_dynamic_source")
    authors = serializers.SerializerMethodField(method_name="get_authors")

    class Meta:
        """Meta class for the ColorSerializer."""

        model = Map
        fields = ("id", "game_item_id", "name", "localizedname", "authors")
