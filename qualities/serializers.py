"""Module contains the serializers for the qualities app."""
from rest_framework import serializers

from qualities.models import Quality


class QualitySerializer(serializers.ModelSerializer):
    """Serializer for the Quality model."""

    class Meta:
        """Meta class for the QualitySerializer."""

        model = Quality
        fields = ("id", "game_item_id", "value")
