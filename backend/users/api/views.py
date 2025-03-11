from django.shortcuts import render, reverse
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib import messages

from rest_framework import viewsets, status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, AllowAny

from treasures.models import Treasure
from treasures.forms import TreasureCreationForm
from .serializers import UserSerializer, SignUpSerializer, LoginSerializer
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
    # authentication_classes = [TokenAuthentication, SessionAuthentication]
    # what goes here for JWT?

    def create(self, request, *args, **kwargs):
        msg = "You can't create a user via this API endpoint. Use the signup endpoint instead."
        return HttpResponse(msg, status=status.HTTP_405_METHOD_NOT_ALLOWED)


class SignupView(CreateAPIView):
    queryset = User.objects.all()
    serializer_class = SignUpSerializer
    permission_classes = [AllowAny]

    def perform_create(self, serializer):
        user = serializer.save()
        # token, _ = Token.objects.get_or_create(user=user)
        return user
        # return token.key

    def create(self, request, *args, **kwargs):
        """Override create method to include the token in the response."""
        # JWT tokens not yet implemented
        return super().create(request, *args, **kwargs)
        # Create user and get token
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        token = self.perform_create(serializer)

        # Get user_data and add token
        user_data = serializer.data
        user_data["token"] = token
        return Response(user_data, status=status.HTTP_201_CREATED)

    def get(self, request):
        msg = (
            "Send a POST request with email, handle (optional), and a "
            "password. Email will function as the username. An auth token "
            "will be returned."
        )
        return Response({"message": msg})


class LoginView(APIView):
    permission_classes = [AllowAny]
    serializer_class = LoginSerializer  # DRF will now auto-generate the form

    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data.get("email")
            password = serializer.validated_data.get("password")
            user = authenticate(email=email, password=password)
            if user:
                return Response({"token": "tokens not yet implemented"})
                return Response({"token": user.auth_token.key})
            return Response(
                {"error": "Invalid credentials"}, status=status.HTTP_401_UNAUTHORIZED
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def get(self, request):
        """Allows for API-GUI form."""
        msg = (
            "Send a POST request with email and password to login and receive a token."
        )
        return Response({"message": msg})


