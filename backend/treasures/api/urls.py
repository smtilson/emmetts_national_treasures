from django.urls import path
from . import views

urlpatterns = [
    path("treasure_list/", views.TreasureListCreate.as_view(), name="treasure_list"),
    path("other_way/", views.get_data, name="other_way"),
    path("other_way_add/", views.add_data, name="other_way_add"),
    path("treasure_access/<int:pk>/", views.TreasureRetrieveUpdateDestroy.as_view(), name="treasure_access"),
]