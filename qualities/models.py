"""Module contains the Quality model for the qualities app."""
from django.db import models
from prefix_id import PrefixIDField

# Create your models here.

class Quality(models.Model):
    """Model for the Quality object."""

    id = PrefixIDField(primary_key=True, prefix="quality")
    game_item_id = models.CharField(max_length=255)
    value = models.CharField(max_length=255)

    def __str__(self) -> str:
        """Representation of the Quality object."""
        return "Quality: " + self.game_item_id + " - " + self.value
