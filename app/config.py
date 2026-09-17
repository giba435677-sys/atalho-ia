from __future__ import annotations

import os
from dataclasses import dataclass

from dotenv import load_dotenv

load_dotenv()


@dataclass(frozen=True)
class Settings:
    tts_voice: str = "pt-br"
    tts_speed: int = 165
    tts_pitch: int = 48
    video_width: int = 1080
    video_height: int = 1920
    video_fps: int = 30


def get_settings() -> Settings:
    return Settings(
        tts_voice=os.getenv("TTS_VOICE", "pt-br"),
        tts_speed=int(os.getenv("TTS_SPEED", "165")),
        tts_pitch=int(os.getenv("TTS_PITCH", "48")),
        video_width=int(os.getenv("VIDEO_WIDTH", "1080")),
        video_height=int(os.getenv("VIDEO_HEIGHT", "1920")),
        video_fps=int(os.getenv("VIDEO_FPS", "30")),
    )
