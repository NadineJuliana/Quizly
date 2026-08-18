from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.test import APITestCase


User = get_user_model()


class AuthenticationUnhappyPathTests(APITestCase):

    def setUp(self):
        self.username = "testuser"
        self.password = "testpassword123"
        self.email = "test@example.com"

    def test_register_user_with_invalid_data(self):
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
        response = self.client.post(
            "/api/token/refresh/",
            {},
            format="json",
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_401_UNAUTHORIZED,
        )