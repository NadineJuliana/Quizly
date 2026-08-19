"""
Tests for successful quiz detail requests.
"""

from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.test import APITestCase
from rest_framework_simplejwt.tokens import RefreshToken

from quiz.models import Quiz, Question


User = get_user_model()


class QuizDetailHappyPathTests(APITestCase):
    """
    Tests successful quiz detail requests.
    """

    def setUp(self):
        """
        Creates and authenticates a user and prepares a quiz with a question.
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

        Question.objects.create(
            quiz=self.quiz,
            question_title="Question 1",
            question_options=[
                "Option A",
                "Option B",
                "Option C",
                "Option D",
            ],
            answer="Option A",
        )

    def test_get_quiz_detail_success(self):
        """
        Tests that an owned quiz can be retrieved successfully.
        """

        response = self.client.get(
            f"/api/quizzes/{self.quiz.id}/"
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
        )

        self.assertEqual(
            response.data["id"],
            self.quiz.id,
        )
        self.assertEqual(
            response.data["title"],
            "Quiz Title",
        )
        self.assertEqual(
            response.data["description"],
            "Quiz Description",
        )
        self.assertEqual(
            response.data["video_url"],
            "https://www.youtube.com/watch?v=example",
        )

        self.assertIn("created_at", response.data)
        self.assertIn("updated_at", response.data)
        self.assertIn("questions", response.data)

        self.assertEqual(
            len(response.data["questions"]),
            1,
        )
