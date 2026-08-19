"""
Serializers for quiz and question data.
"""

from rest_framework import serializers

from quiz.models import Quiz, Question


class QuestionSerializer(serializers.ModelSerializer):
    """
    Serializes question data.
    """

    class Meta:
        """
        Defines the model fields included in question responses.
        """

        model = Question
        fields = [
            "id",
            "question_title",
            "question_options",
            "answer",
            "created_at",
            "updated_at",
        ]


class QuizSerializer(serializers.ModelSerializer):
    """
    Serializes quiz data together with its related questions.
    """

    questions = QuestionSerializer(many=True, read_only=True)

    class Meta:
        """
        Defines the model fields included in quiz responses.
        """

        model = Quiz
        fields = [
            "id",
            "title",
            "description",
            "created_at",
            "updated_at",
            "video_url",
            "questions",
        ]


class QuizCreateSerializer(serializers.Serializer):
    """
    Validates the YouTube URL used to create a quiz.
    """

    url = serializers.URLField()
