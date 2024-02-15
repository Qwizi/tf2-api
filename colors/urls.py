"""URLs for the colors app."""
from django.urls import path

from colors import views

urlpatterns = [
    path("", views.ColorList.as_view(), name="color-list"),
]
