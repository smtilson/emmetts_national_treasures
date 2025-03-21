from rest_framework import serializers, status
from rest_framework.exceptions import AuthenticationFailed
from rest_framework.validators import UniqueValidator
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from django.contrib.auth.password_validation import validate_password
from django.contrib.auth import get_user_model, authenticate
from django.conf import settings
import sys


User = get_user_model()
DEBUG = settings.DEBUG
TEST = "test" in sys.argv


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        exclude = [
            "password",
            "groups",
            "user_permissions",
        ]
        read_only_fields = [
            "id",
            "is_staff",
            "is_active",
            "is_superuser",
            "date_joined",
        ]

    def create(self, validated_data):
        raise NotImplementedError(
            "Use UserSerializer for update and read. Use SignUpSerializer for user creation."
        )


class SignUpSerializer(serializers.ModelSerializer):
    password = serializers.CharField(
        write_only=True,
        required=True,
        validators=[] if DEBUG else [validate_password],
    )
    handle = serializers.CharField(
        required=False, validators=[UniqueValidator(queryset=User.objects.all())]
    )
    email = serializers.EmailField(
        validators=[UniqueValidator(queryset=User.objects.all())]
    )

    class Meta:
        model = User
        fields = [
            "email",
            "handle",
            "password",
        ]

    def create(self, validated_data):
        # Hashes password before save
        return User.objects.create_user(**validated_data)

    def update(self, instance, validated_data):
        raise NotImplementedError(
            "Use SignUpSerializer for user creation. Use UserSerializer for updates."
        )


class LoginSerializer(TokenObtainPairSerializer):
    username_field = "email"

    def validate(self, data):
        token_data = super().validate(data)
        data = {
            "id": self.user.id,
            "email": self.user.email,
            "handle": getattr(self.user, "handle", ""),
        }
        data.update(token_data)
        # except AuthenticationFailed as e:
        #   raise serializers.ValidationError(
        #      {"detail": str(e)}, code=status.HTTP_401_UNAUTHORIZED
        # )
        return data
