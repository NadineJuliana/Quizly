"""
Tests for unsuccessful quiz detail requests.
"""

from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.test import APITestCase
from rest_framework_simplejwt.tokens import RefreshToken

from quiz.models import Quiz


User = get_user_model()


class QuizDetailUnhappyPathTests(APITestCase):
    """
    Tests unsuccessful quiz detail requests.
    """

    def setUp(self):
        """
        Creates users required for quiz detail permission tests.
        """

        self.user = User.objects.create_user(
            username="testuser",
            password="testpassword123",
            email="test@example.com",
        )

        self.other_user = User.objects.create_user(
            username="otheruser",
            password="testpassword123",
            email="other@example.com",
        )

    def authenticate_user(self):
        """
        Authenticates the test user using an access token.
        """

        refresh = RefreshToken.for_user(self.user)
        self.client.cookies["access_token"] = str(refresh.access_token)

    def test_get_quiz_detail_without_authentication(self):
        """
        Tests that quiz details cannot be retrieved without authentication.
        """

        quiz = Quiz.objects.create(
            user=self.user,
            title="Quiz Title",
            description="Quiz Description",
            video_url="https://www.youtube.com/watch?v=example",
        )

        response = self.client.get(
            f"/api/quizzes/{quiz.id}/"
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_401_UNAUTHORIZED,
        )

    def test_get_quiz_detail_forbidden(self):
        """
        Tests that a user cannot access another user's quiz.
        """

        self.authenticate_user()

        quiz = Quiz.objects.create(
            user=self.other_user,
            title="Other Quiz",
            description="Other Description",
            video_url="https://www.youtube.com/watch?v=example",
        )

        response = self.client.get(
            f"/api/quizzes/{quiz.id}/"
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_403_FORBIDDEN,
        )

    def test_get_quiz_detail_not_found(self):
        """
        Tests that requesting a nonexistent quiz returns status 404.
        """

        self.authenticate_user()

        response = self.client.get(
            "/api/quizzes/9999/"
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_404_NOT_FOUND,
        )
