from httpx import request
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from authentication.api.authentication import CookieJWTAuthentication
from quiz.api.serializers import (
    QuizCreateSerializer,
    QuizSerializer,
)
from quiz.models import Quiz, Question
from quiz.services import create_quiz_from_youtube

# Create your views here.


class QuizListCreateView(APIView):
    authentication_classes = [CookieJWTAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request):
        input_serializer = QuizCreateSerializer(data=request.data)
        input_serializer.is_valid(raise_exception=True)

        url = input_serializer.validated_data["url"]

        quiz_data = create_quiz_from_youtube(url)

        quiz = Quiz.objects.create(
            user=request.user,
            title=quiz_data["title"],
            description=quiz_data["description"],
            video_url=quiz_data["video_url"],
        )

        for question_data in quiz_data["questions"]:
            Question.objects.create(
                quiz=quiz,
                **question_data,
            )

        serializer = QuizSerializer(quiz)

        return Response(
            serializer.data,
            status=status.HTTP_201_CREATED,
        )

    def get(self, request):
        quizzes = Quiz.objects.filter(user=request.user)

        serializer = QuizSerializer(
            quizzes,
            many=True,
        )

        return Response(
            serializer.data,
            status=status.HTTP_200_OK,
        )


class QuizDetailView(APIView):
    authentication_classes = [CookieJWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request, pk):
        try:
            quiz = Quiz.objects.get(pk=pk)
        except Quiz.DoesNotExist:
            return Response(
                {"detail": "Quiz not found."},
                status=status.HTTP_404_NOT_FOUND,
            )

        if quiz.user != request.user:
            return Response(
                {"detail": "You do not have permission to access this quiz."},
                status=status.HTTP_403_FORBIDDEN,
            )

        serializer = QuizSerializer(quiz)

        return Response(
            serializer.data,
            status=status.HTTP_200_OK,
        )

    def patch(self, request, pk):
        try:
            quiz = Quiz.objects.get(pk=pk)
        except Quiz.DoesNotExist:
            return Response(
                {"detail": "Quiz not found."},
                status=status.HTTP_404_NOT_FOUND,
            )

        if quiz.user != request.user:
            return Response(
                {"detail": "You do not have permission to access this quiz."},
                status=status.HTTP_403_FORBIDDEN,
            )

        serializer = QuizSerializer(
            quiz,
            data=request.data,
            partial=True,
        )

        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(
            serializer.data,
            status=status.HTTP_200_OK,
        )

    def delete(self, request, pk):
        try:
            quiz = Quiz.objects.get(pk=pk)
        except Quiz.DoesNotExist:
            return Response(
                {"detail": "Quiz not found."},
                status=status.HTTP_404_NOT_FOUND,
            )

        if quiz.user != request.user:
            return Response(
                {"detail": "You do not have permission to access this quiz."},
                status=status.HTTP_403_FORBIDDEN,
            )

        quiz.delete()

        return Response(
            status=status.HTTP_204_NO_CONTENT,
        )
