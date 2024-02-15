"""Serializers for the colors app."""
from rest_framework import serializers

from colors.models import Color


class ColorSerializer(serializers.ModelSerializer):
    """Serializer for the Color model."""

    class Meta:
        """Meta class for the ColorSerializer."""

        model = Color
        fields = ("id", "game_item_id", "color_name", "color_hex")
