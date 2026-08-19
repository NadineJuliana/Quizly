"""
Tests for successful quiz update requests.
"""

from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.test import APITestCase
from rest_framework_simplejwt.tokens import RefreshToken

from quiz.models import Quiz


User = get_user_model()


class QuizUpdateHappyPathTests(APITestCase):
    """
    Tests successful quiz update requests.
    """

    def setUp(self):
        """
        Creates and authenticates a user and prepares a quiz for updating.
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

    def test_update_quiz_success(self):
        """
        Tests that an owned quiz can be partially updated successfully.
        """

        data = {
            "title": "Partially Updated Title",
            "description": "Partially Updated Description",
        }

        response = self.client.patch(
            f"/api/quizzes/{self.quiz.id}/",
            data,
            format="json",
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
        )

        self.assertEqual(
            response.data["title"],
            "Partially Updated Title",
        )
        self.assertEqual(
            response.data["description"],
            "Partially Updated Description",
        )

        self.assertEqual(
            response.data["video_url"],
            self.quiz.video_url,
        )

        self.assertIn("id", response.data)
        self.assertIn("created_at", response.data)
        self.assertIn("updated_at", response.data)
        self.assertIn("questions", response.data)
