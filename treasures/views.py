from django.shortcuts import render
from django.http import HttpResponse
from rest_framework import generics
from .models import Treasure
from .serializers import TreasureSerializer
# Create your views here.

class TreasureListCreate(generics.ListCreateAPIView):
    queryset = Treasure.objects.all()
    serializer_class = TreasureSerializer