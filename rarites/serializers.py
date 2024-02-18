"""Serializers for the colors app."""
from rest_framework import serializers

from colors.serializers import ColorSerializer
from rarites.models import Rarity


class RaritySerializer(serializers.ModelSerializer):
    """Serializer for the Color model."""

    color = ColorSerializer(read_only=True)
    class Meta:
        """Meta class for the ColorSerializer."""

        model = Rarity
        fields = ("id", "game_item_id", "value", "loc_key", "loc_key_weapon", "color", "next_rarity")
        depth = 1
