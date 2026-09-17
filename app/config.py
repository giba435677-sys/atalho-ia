from __future__ import annotations

import os
from dataclasses import dataclass

from dotenv import load_dotenv

load_dotenv()


@dataclass(frozen=True)
class Settings:
    tts_model: str = ".cache/piper/pt_BR-faber-medium.onnx"
    video_width: int = 1080
    video_height: int = 1920
    video_fps: int = 30


def get_settings() -> Settings:
    return Settings(
        tts_model=os.getenv("TTS_MODEL", ".cache/piper/pt_BR-faber-medium.onnx"),
        video_width=int(os.getenv("VIDEO_WIDTH", "1080")),
        video_height=int(os.getenv("VIDEO_HEIGHT", "1920")),
        video_fps=int(os.getenv("VIDEO_FPS", "30")),
    )
