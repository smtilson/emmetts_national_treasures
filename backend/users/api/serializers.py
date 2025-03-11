from rest_framework import serializers
from rest_framework.exceptions import AuthenticationFailed
from rest_framework.validators import UniqueValidator
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


class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        email = data.get("email")
        password = data.get("password")

        if email and password:
            user = authenticate(
                request=self.context.get("request"), email=email, password=password
            )
            if not user:
                raise AuthenticationFailed("Invalid email or password.")
            data["user"] = user
        else:
            raise serializers.ValidationError("Both email and password are required.")
        return data
