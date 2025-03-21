from django.shortcuts import render, reverse
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib import messages

from rest_framework import viewsets, status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, AllowAny, IsAdminUser
from rest_framework.authentication import SessionAuthentication
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.authentication import JWTAuthentication

from treasures.models import Treasure
from treasures.forms import TreasureCreationForm
from .serializers import UserSerializer, SignUpSerializer, LoginSerializer
from .permissions import IsOwnerOrAdmin, IsFriend
from rest_framework.generics import CreateAPIView
from django.contrib.auth import get_user_model, authenticate

User = get_user_model()


# need to add things that check request.method and then redirect and what not.
# also flow control to check that users are valid or authenticated.


# Create your views here.
class UserViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]  # IsSuperUser
    queryset = User.objects.all().order_by("date_joined")
    serializer_class = UserSerializer
    authentication_classes = [JWTAuthentication, SessionAuthentication]


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all().order_by("date_joined")
    serializer_class = UserSerializer
    
    def get_permissions(self):
        """
        Instantiates and returns the list of permissions that this view requires.
        """
        if self.action in ['update', 'partial_update', 'destroy']:
            permission_classes = [IsAuthenticated, IsOwnerOrAdmin]
        else:
            permission_classes = [IsAuthenticated]
        return [permission() for permission in permission_classes]

    def create(self, request, *args, **kwargs):
        msg = "You can't create a user via this API endpoint. Use the signup endpoint instead."
        return HttpResponse(msg, status=status.HTTP_405_METHOD_NOT_ALLOWED)


class SignupView(CreateAPIView):
    queryset = User.objects.all()
    serializer_class = SignUpSerializer
    permission_classes = [AllowAny]

    def perform_create(self, serializer):
        user = serializer.save()
        return user

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = self.perform_create(serializer)

        refresh = RefreshToken.for_user(user)
        data = serializer.data
        data["access"] = str(refresh.access_token)
        data["refresh"] = str(refresh)
        return Response(data, status=status.HTTP_201_CREATED)

    def get(self, request):
        msg = (
            "Send a POST request with email, handle (optional), and a "
            "password. Email will function as the username. Access and refresh tokens "
            "will be returned."
        )
        return Response({"message": msg})


class LoginView(APIView):
    permission_classes = [AllowAny]
    serializer_class = LoginSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        return Response(serializer.validated_data)

    def get(self, request):
        msg = (
            "Send a POST request with email and password. Email will function as the username. "
            "Access and refresh tokens will be returned."
        )
        return Response({"message": msg})
