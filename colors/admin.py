"""Module registers the Color model with the Django admin site."""
from django.contrib import admin

from colors.models import Color

admin.site.register(Color)
