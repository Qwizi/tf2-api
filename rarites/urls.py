"""URLs for the qualities app."""
from django.urls import path

from rarites import views

urlpatterns = [
    path("", views.RarityList.as_view(), name="rarity-list"),
]
