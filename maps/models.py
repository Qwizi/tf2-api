"""Models for the maps app."""
from django.db import models
from django.utils.translation import gettext_lazy as _
from prefix_id import PrefixIDField

# Create your models here.

class Map(models.Model):
    """Model for a map."""

    id = PrefixIDField(primary_key=True, prefix="map")
    game_item_id = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    localizedname = models.CharField(max_length=255, help_text=_("The localized name of the map."))
    authors = models.CharField(max_length=255, help_text=_("The authors of the map."), blank=True)

    def __str__(self) -> str:
        """Representation of the Map object."""
        return "Map: " + self.game_item_id + " - " + self.name

    def get_localized_name(self) -> str:
        """Get the localized name of the map."""
        return _(self.localizedname)
