"""
Tests for unsuccessful quiz creation requests.
"""

from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.test import APITestCase
from rest_framework_simplejwt.tokens import RefreshToken


User = get_user_model()


class QuizCreateUnhappyPathTests(APITestCase):
    """
    Tests unsuccessful quiz creation requests.
    """

    def setUp(self):
        """
        Creates a user and prepares the quiz creation endpoint.
        """

        self.user = User.objects.create_user(
            username="testuser",
            password="testpassword123",
            email="test@example.com",
        )

        self.url = "/api/quizzes/"

    def test_create_quiz_with_invalid_data(self):
        """
        Tests that quiz creation fails when invalid data is provided.
        """

        refresh = RefreshToken.for_user(self.user)
        self.client.cookies["access_token"] = str(refresh.access_token)

        response = self.client.post(
            self.url,
            {},
            format="json",
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_400_BAD_REQUEST,
        )

    def test_create_quiz_without_authentication(self):
        """
        Tests that quiz creation fails without authentication.
        """

        data = {
            "url": "https://www.youtube.com/watch?v=example",
        }

        response = self.client.post(
            self.url,
            data,
            format="json",
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_401_UNAUTHORIZED,
        )
