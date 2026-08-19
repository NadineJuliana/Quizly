from rest_framework import status
from rest_framework.test import APITestCase


class QuizListUnhappyPathTests(APITestCase):

    def test_get_quizzes_without_authentication(self):
        response = self.client.get("/api/quizzes/")

        self.assertEqual(
            response.status_code,
            status.HTTP_401_UNAUTHORIZED,
        )
