from django.contrib import admin

from quiz.models import Quiz, Question

# Register your models here.


@admin.register(Quiz)
class QuizAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "title",
        "user",
        "video_url",
        "created_at",
    )

    search_fields = (
        "title",
        "user__username",
        "video_url",
    )


@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "question_title",
        "quiz",
        "answer",
        "created_at",
    )

    search_fields = (
        "question_title",
        "quiz__title",
        "answer",
    )
