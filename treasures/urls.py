from django.urls import path
from . import views

urlpatterns = [
    path("treasure_list/", views.TreasureListCreate.as_view(), name="treasure_list"),
]