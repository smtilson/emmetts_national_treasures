from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import CommentViewSet

router = DefaultRouter()
router.register(
    r"treasures/(?P<treasure_pk>\d+)/comments", CommentViewSet, basename="comment"
)

urlpatterns = [
    path("api/", include(router.urls)),
]
