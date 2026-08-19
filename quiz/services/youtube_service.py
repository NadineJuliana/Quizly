"""
Service for downloading and extracting audio from YouTube videos.
"""

from pathlib import Path
import tempfile

import yt_dlp


def download_audio(url):
    """
    Downloads a YouTube video and extracts its audio as an MP3 file.
    """

    temp_dir = tempfile.mkdtemp()

    tmp_filename = str(
        Path(temp_dir) / "%(id)s.%(ext)s"
    )

    ydl_opts = {
        "format": "18",
        "outtmpl": tmp_filename,
        "quiet": True,
        "noplaylist": True,
        "force_ipv4": True,
        "js_runtimes": {
            "node": {},
        },
        "extractor_args": {
            "youtube": {
                "player_client": ["mweb"],
            }
        },
        "postprocessors": [
            {
                "key": "FFmpegExtractAudio",
                "preferredcodec": "mp3",
                "preferredquality": "192",
            }
        ],
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=True)

    video_id = info["id"]

    audio_path = Path(temp_dir) / f"{video_id}.mp3"

    video_url = (
        f"https://www.youtube.com/watch?v={video_id}"
    )

    return {
        "audio_path": str(audio_path),
        "video_url": video_url,
    }
