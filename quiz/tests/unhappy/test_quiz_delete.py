# quiz/tests/unhappy/test_quiz_delete.py

from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.test import APITestCase
from rest_framework_simplejwt.tokens import RefreshToken

from quiz.models import Quiz


User = get_user_model()


class QuizDeleteUnhappyPathTests(APITestCase):

    def setUp(self):
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
        refresh = RefreshToken.for_user(self.user)
        self.client.cookies["access_token"] = str(refresh.access_token)

    def test_delete_quiz_without_authentication(self):
        quiz = Quiz.objects.create(
            user=self.user,
            title="Quiz Title",
            description="Quiz Description",
            video_url="https://www.youtube.com/watch?v=example",
        )

        response = self.client.delete(
            f"/api/quizzes/{quiz.id}/"
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_401_UNAUTHORIZED,
        )

    def test_delete_quiz_forbidden(self):
        self.authenticate_user()

        quiz = Quiz.objects.create(
            user=self.other_user,
            title="Other Quiz",
            description="Other Description",
            video_url="https://www.youtube.com/watch?v=example",
        )

        response = self.client.delete(
            f"/api/quizzes/{quiz.id}/"
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_403_FORBIDDEN,
        )

    def test_delete_quiz_not_found(self):
        self.authenticate_user()

        response = self.client.delete(
            "/api/quizzes/9999/"
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_404_NOT_FOUND,
        )