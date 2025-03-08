from rest_framework.viewsets import ModelViewSet
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from ..models import Comment
from .serializers import CommentSerializer
from treasures.models import Treasure


# Create your views here.
class CommentViewSet(ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer

    # perhaps the treasure_id should be passed in the url?
    def get_queryset(self):
        return Comment.objects.filter(treasure=self.kwargs["treasure_pk"])

    def perform_create(self, serializer):
        treasure = Treasure.objects.get(pk=self.kwargs["treasure_pk"])
        serializer.save(user=self.request.user, treasure=treasure)
