"""
Tests for successful quiz deletion requests.
"""

from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.test import APITestCase
from rest_framework_simplejwt.tokens import RefreshToken

from quiz.models import Quiz


User = get_user_model()


class QuizDeleteHappyPathTests(APITestCase):
    """
    Tests successful quiz deletion requests.
    """

    def setUp(self):
        """
        Creates and authenticates a user and prepares a quiz for deletion.
        """

        self.user = User.objects.create_user(
            username="testuser",
            password="testpassword123",
            email="test@example.com",
        )

        refresh = RefreshToken.for_user(self.user)
        self.client.cookies["access_token"] = str(refresh.access_token)

        self.quiz = Quiz.objects.create(
            user=self.user,
            title="Quiz Title",
            description="Quiz Description",
            video_url="https://www.youtube.com/watch?v=example",
        )

    def test_delete_quiz_success(self):
        """
        Tests that a user can delete an owned quiz successfully.
        """

        response = self.client.delete(
            f"/api/quizzes/{self.quiz.id}/"
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_204_NO_CONTENT,
        )

        self.assertFalse(
            Quiz.objects.filter(pk=self.quiz.id).exists()
        )
