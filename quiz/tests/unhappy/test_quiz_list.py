"""
Tests for unsuccessful quiz list requests.
"""

from rest_framework import status
from rest_framework.test import APITestCase


class QuizListUnhappyPathTests(APITestCase):
    """
    Tests unsuccessful quiz list requests.
    """

    def test_get_quizzes_without_authentication(self):
        """
        Tests that quizzes cannot be retrieved without authentication.
        """

        response = self.client.get("/api/quizzes/")

        self.assertEqual(
            response.status_code,
            status.HTTP_401_UNAUTHORIZED,
        )
