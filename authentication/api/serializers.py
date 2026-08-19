"""
Serializers for user registration and login.
"""

from django.contrib.auth import authenticate, get_user_model
from rest_framework import serializers


User = get_user_model()


class RegistrationSerializer(serializers.ModelSerializer):
    """
    Validates registration data and creates a new user account.
    """

    confirmed_password = serializers.CharField(write_only=True)

    class Meta:
        """
        Defines the model fields used for user registration.
        """

        model = User
        fields = [
            "username",
            "password",
            "confirmed_password",
            "email",
        ]
        extra_kwargs = {
            "password": {"write_only": True}
        }

    def validate(self, attrs):
        """
        Checks whether both submitted passwords match.
        """

        if attrs["password"] != attrs["confirmed_password"]:
            raise serializers.ValidationError(
                {"confirmed_password": "Passwords do not match."}
            )

        return attrs

    def create(self, validated_data):
        """
        Creates a new user with the validated registration data.
        """

        validated_data.pop("confirmed_password")

        return User.objects.create_user(**validated_data)


class LoginSerializer(serializers.Serializer):
    """
    Authenticates a user using the provided credentials.
    """

    username = serializers.CharField()
    password = serializers.CharField(write_only=True)

    def validate(self, attrs):
        """
        Verifies the username and password combination.
        """

        user = authenticate(
            username=attrs["username"],
            password=attrs["password"],
        )

        if not user:
            raise serializers.ValidationError(
                {"detail": "Invalid credentials."}
            )

        attrs["user"] = user
        return attrs
