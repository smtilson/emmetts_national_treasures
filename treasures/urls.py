from django.urls import path
from . import views

urlpatterns = [
    path("add_treasure", views.add_treasure, name="add_treasure"),
]