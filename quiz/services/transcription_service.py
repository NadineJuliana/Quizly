"""
Service for transcribing audio files using Whisper.
"""

import whisper

_model = None


def get_whisper_model():
    """
    Loads and returns the Whisper model instance.
    """

    global _model

    if _model is None:
        _model = whisper.load_model("turbo")

    return _model


def transcribe_audio(audio_path):
    """
    Transcribes an audio file and returns the generated text.
    """

    model = get_whisper_model()

    result = model.transcribe(
        audio_path,
        fp16=False,
    )

    return result["text"]
