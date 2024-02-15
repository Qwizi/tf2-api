"""URLs for the qualities app."""
from django.urls import path

from qualities import views

urlpatterns = [
    path("", views.QualityList.as_view(), name="quality-list"),
]
