from rest_framework import serializers
from rest_framework.exceptions import AuthenticationFailed
from django.contrib.auth.password_validation import validate_password
from django.contrib.auth import get_user_model, authenticate

User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = "__all__"
        read_only_fields = [
            "id",
            "groups",
            "user_permissions",
            "is_staff",
            "is_superuser",
            "is_active",
            "date_joined",
            "last_login",
        ]


class SignUpSerializer(serializers.ModelSerializer):
    password = serializers.CharField(
        write_only=True, required=True, validators=[validate_password]
    )
    handle = serializers.CharField(required=False)

    class Meta:
        model = User
        fields = [
            "handle",
            "email",
            "password",
        ]

    def create(self, validated_data):
        return User.objects.create_user(**validated_data)


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
