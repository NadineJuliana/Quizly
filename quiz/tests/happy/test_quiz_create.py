from unittest.mock import patch

from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.test import APITestCase
from rest_framework_simplejwt.tokens import RefreshToken


User = get_user_model()


class QuizCreateHappyPathTests(APITestCase):

    def setUp(self):
        self.user = User.objects.create_user(
            username="testuser",
            password="testpassword123",
            email="test@example.com",
        )

        refresh = RefreshToken.for_user(self.user)

        self.client.cookies["access_token"] = str(refresh.access_token)
        self.client.cookies["refresh_token"] = str(refresh)

        self.url = "/api/quizzes/"
        self.video_url = "https://www.youtube.com/watch?v=example"

    @patch(
        "quiz.api.views.create_quiz_from_youtube",
        create=True,
    )
    def test_create_quiz_success(self, mock_create_quiz):
        mock_create_quiz.return_value = {
            "title": "Quiz Title",
            "description": "Quiz Description",
            "questions": [
                {
                    "question_title": "Question 1",
                    "question_options": [
                        "Option A",
                        "Option B",
                        "Option C",
                        "Option D",
                    ],
                    "answer": "Option A",
                }
            ],
        }

        data = {
            "url": self.video_url,
        }

        response = self.client.post(
            self.url,
            data,
            format="json",
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_201_CREATED,
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
            self.video_url,
        )

        self.assertIn("id", response.data)
        self.assertIn("created_at", response.data)
        self.assertIn("updated_at", response.data)
        self.assertIn("questions", response.data)

        self.assertEqual(
            len(response.data["questions"]),
            1,
        )

        question = response.data["questions"][0]

        self.assertIn("id", question)
        self.assertIn("created_at", question)
        self.assertIn("updated_at", question)

        self.assertEqual(
            question["question_title"],
            "Question 1",
        )
        self.assertEqual(
            question["question_options"],
            [
                "Option A",
                "Option B",
                "Option C",
                "Option D",
            ],
        )
        self.assertEqual(
            question["answer"],
            "Option A",
        )
