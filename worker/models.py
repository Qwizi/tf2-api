from django.db import models
from prefix_id import PrefixIDField


class TrackFile(models.Model):
    """Model for a map."""

    id = PrefixIDField(primary_key=True, prefix="file")
    file_name = models.CharField(max_length=255)
    last_modified = models.DateTimeField(null=True, blank=True)

    def __str__(self) -> str:
        """Representation of the Map object."""
        return "File: " + self.file_name + " - " + str(self.last_modified)
