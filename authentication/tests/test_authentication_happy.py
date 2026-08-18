from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.test import APITestCase
from rest_framework_simplejwt.tokens import RefreshToken


User = get_user_model()


class AuthenticationHappyPathTests(APITestCase):

    def setUp(self):
        self.username = "testuser"
        self.password = "testpassword123"
        self.email = "test@example.com"

    def test_register_user_success(self):
        data = {
            "username": self.username,
            "password": self.password,
            "confirmed_password": self.password,
            "email": self.email,
        }

        response = self.client.post("/api/register/", data, format="json")

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(
            response.data,
            {"detail": "User created successfully!"}
        )
        self.assertTrue(
            User.objects.filter(
                username=self.username,
                email=self.email
            ).exists()
        )

    def test_login_success(self):
        user = User.objects.create_user(
            username=self.username,
            password=self.password,
            email=self.email,
        )

        data = {
            "username": self.username,
            "password": self.password,
        }

        response = self.client.post("/api/login/", data, format="json")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            response.data,
            {
                "detail": "Login successfully!",
                "user": {
                    "id": user.id,
                    "username": self.username,
                    "email": self.email,
                }
            }
        )
        self.assertIn("access_token", response.cookies)
        self.assertIn("refresh_token", response.cookies)

    def test_logout_success(self):
        user = User.objects.create_user(
            username=self.username,
            password=self.password,
            email=self.email,
        )

        refresh = RefreshToken.for_user(user)

        self.client.cookies["access_token"] = str(refresh.access_token)
        self.client.cookies["refresh_token"] = str(refresh)

        response = self.client.post("/api/logout/", {}, format="json")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            response.data,
            {
                "detail": (
                    "Log-Out successfully! All Tokens will be deleted. "
                    "Refresh token is now invalid."
                )
            }
        )

        self.assertEqual(response.cookies["access_token"].value, "")
        self.assertEqual(response.cookies["refresh_token"].value, "")

    def test_refresh_token_success(self):
        user = User.objects.create_user(
            username=self.username,
            password=self.password,
            email=self.email,
        )

        refresh = RefreshToken.for_user(user)
        self.client.cookies["refresh_token"] = str(refresh)

        response = self.client.post(
            "/api/token/refresh/",
            {},
            format="json"
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            response.data,
            {"detail": "Token refreshed"}
        )
        self.assertIn("access_token", response.cookies)