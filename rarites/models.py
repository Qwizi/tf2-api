"""Models for the rarites app."""
from django.db import models
from prefix_id import PrefixIDField


# Create your models here.
class Rarity(models.Model):
    """Model for a rarity."""

    id = PrefixIDField(primary_key=True, prefix="rarity")
    game_item_id = models.CharField(max_length=255)
    value = models.CharField(max_length=255)
    loc_key = models.CharField(max_length=255)
    loc_key_weapon = models.CharField(max_length=255)
    color = models.ForeignKey("colors.Color", on_delete=models.CASCADE)
    next_rarity = models.ForeignKey("self", on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self) -> str:
        """Representation of the Rarity object."""
        return "Rarity: " + self.game_item_id + " - " + self.value
