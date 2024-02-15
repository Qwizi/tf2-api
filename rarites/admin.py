"""Module for admin site configuration."""
from django.contrib import admin

from rarites.models import Rarity

# Register your models here.

admin.site.register(Rarity)