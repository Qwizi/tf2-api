"""URLs for the colors app."""
from django.urls import path

from maps import views

urlpatterns = [
    path("", views.MapList.as_view(), name="map-list"),
]
