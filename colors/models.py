"""Color model for the colors app."""
from django.db import models
from prefix_id import PrefixIDField


# Create your models here.
class Color(models.Model):
    """Model for a color."""

    id = PrefixIDField(primary_key=True, prefix="color")
    game_item_id = models.CharField(max_length=255)
    color_name = models.CharField(max_length=255)
    color_hex = models.CharField(max_length=7)

    def __str__(self) -> str:
        """Representation of the Color object."""
        return f"{self.game_item_id} - {self.color_hex}"
