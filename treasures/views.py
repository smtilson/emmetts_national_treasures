from django.shortcuts import render
from django.http import HttpResponse
from rest_framework import generics
from rest_framework.response import Response
from rest_framework.decorators import api_view
from .models import Treasure
from .serializers import TreasureSerializer
# Create your views here.

#there are other ways of doing this such as
@api_view(['GET'])
def get_data(request):
    treasures = Treasure.objects.all()
    serializer = TreasureSerializer(treasures, many=True)
    return Response(serializer.data)

@api_view(['POST'])
def add_data(request):
    creator_id = request.user.id
    data = request.data
    data["creator_id"] = 1
    serializer = TreasureSerializer(data=data)
    print(data)
    print(serializer.initial_data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    print(data)
    return Response(serializer.errors)

class TreasureListCreate(generics.ListCreateAPIView):
    queryset = Treasure.objects.all()
    serializer_class = TreasureSerializer
    
class TreasureRetrieveUpdateDestroy(generics.RetrieveUpdateDestroyAPIView):
    queryset = Treasure.objects.all()
    serializer_class = TreasureSerializer
    lookup_field = "pk"