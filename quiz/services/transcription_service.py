import whisper


_model = None


def get_whisper_model():
    global _model

    if _model is None:
        _model = whisper.load_model("turbo")

    return _model


def transcribe_audio(audio_path):
    model = get_whisper_model()

    result = model.transcribe(
        audio_path,
        fp16=False,
    )

    return result["text"]
