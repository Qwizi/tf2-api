"""Module registers the Quality model with the Django admin site."""
from django.contrib import admin

from qualities.models import Quality

# Register your models here.
admin.site.register(Quality)
