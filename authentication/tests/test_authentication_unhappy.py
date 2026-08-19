"""
Tests for unsuccessful authentication requests.
"""

from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.test import APITestCase


User = get_user_model()


class AuthenticationUnhappyPathTests(APITestCase):
    """
    Tests unsuccessful authentication requests.
    """

    def setUp(self):
        """
        Prepares reusable user data for authentication tests.
        """

        self.username = "testuser"
        self.password = "testpassword123"
        self.email = "test@example.com"

    def test_register_user_with_invalid_data(self):
        """
        Tests that registration fails when the passwords do not match.
        """

        data = {
            "username": self.username,
            "password": self.password,
            "confirmed_password": "differentpassword",
            "email": self.email,
        }

        response = self.client.post(
            "/api/register/",
            data,
            format="json",
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_400_BAD_REQUEST,
        )

    def test_login_with_invalid_credentials(self):
        """
        Tests that login fails when invalid credentials are provided.
        """

        User.objects.create_user(
            username=self.username,
            password=self.password,
            email=self.email,
        )

        data = {
            "username": self.username,
            "password": "wrongpassword",
        }

        response = self.client.post(
            "/api/login/",
            data,
            format="json",
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_401_UNAUTHORIZED,
        )

    def test_logout_without_authentication(self):
        """
        Tests that logout fails when the user is not authenticated.
        """

        response = self.client.post(
            "/api/logout/",
            {},
            format="json",
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_401_UNAUTHORIZED,
        )

    def test_refresh_token_without_valid_token(self):
        """
        Tests that token refresh fails without a valid refresh token.
        """

        response = self.client.post(
            "/api/token/refresh/",
            {},
            format="json",
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_401_UNAUTHORIZED,
        )
