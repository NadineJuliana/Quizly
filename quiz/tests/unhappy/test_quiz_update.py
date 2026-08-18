from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.test import APITestCase
from rest_framework_simplejwt.tokens import RefreshToken

from quiz.models import Quiz


User = get_user_model()


class QuizUpdateUnhappyPathTests(APITestCase):

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

    def test_update_quiz_with_invalid_data(self):
        self.authenticate_user()

        quiz = Quiz.objects.create(
            user=self.user,
            title="Quiz Title",
            description="Quiz Description",
            video_url="https://www.youtube.com/watch?v=example",
        )

        data = {
            "title": "",
        }

        response = self.client.patch(
            f"/api/quizzes/{quiz.id}/",
            data,
            format="json",
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_400_BAD_REQUEST,
        )

    def test_update_quiz_without_authentication(self):
        quiz = Quiz.objects.create(
            user=self.user,
            title="Quiz Title",
            description="Quiz Description",
            video_url="https://www.youtube.com/watch?v=example",
        )

        response = self.client.patch(
            f"/api/quizzes/{quiz.id}/",
            {"title": "Updated Title"},
            format="json",
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_401_UNAUTHORIZED,
        )

    def test_update_quiz_forbidden(self):
        self.authenticate_user()

        quiz = Quiz.objects.create(
            user=self.other_user,
            title="Other Quiz",
            description="Other Description",
            video_url="https://www.youtube.com/watch?v=example",
        )

        response = self.client.patch(
            f"/api/quizzes/{quiz.id}/",
            {"title": "Updated Title"},
            format="json",
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_403_FORBIDDEN,
        )

    def test_update_quiz_not_found(self):
        self.authenticate_user()

        response = self.client.patch(
            "/api/quizzes/9999/",
            {"title": "Updated Title"},
            format="json",
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_404_NOT_FOUND,
        )
