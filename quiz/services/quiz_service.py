"""
Service for creating quizzes from YouTube videos.
"""

from .youtube_service import download_audio
from .transcription_service import transcribe_audio
from .quiz_generation_service import generate_quiz


def create_quiz_from_youtube(url):
    """
    Creates quiz data from the audio content of a YouTube video.
    """

    video_data = download_audio(url)

    transcript = transcribe_audio(
        video_data["audio_path"]
    )

    quiz_data = generate_quiz(transcript)

    return {
        "title": quiz_data["title"],
        "description": quiz_data["description"],
        "video_url": video_data["video_url"],
        "questions": quiz_data["questions"],
    }
