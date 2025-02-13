from django.shortcuts import render
from django.http import HttpResponse
from rest_framework import generics, viewsets
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework.permissions import IsAuthenticated
from ..models import Treasure
from .serializers import TreasureSerializer
# Create your views here.


class TreasureViewSet(viewsets.ModelViewSet):
    queryset = Treasure.objects.all()
    serializer_class = TreasureSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Treasure.objects.filter(creator=self.request.user)

    def perform_create(self, serializer):
        serializer.save(creator=self.request.user)


def copy_treasure(request, pk):
    treasure = Treasure.objects.get(pk=pk)
    treasure_dict = TreasureSerializer(instance=treasure).data
    new_treasure_data = {
        key: value for key, value in treasure_dict.items() if key not in treasure.ignore
    }
    new_treasure = Treasure.objects.create(creator=request.user, **new_treasure_data)
    new_treasure.save()
    # should there be some error handling here?
    # feedback to the user?
    return HttpResponse("Treasure copied")
