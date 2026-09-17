from __future__ import annotations

import os
from dataclasses import dataclass

from dotenv import load_dotenv

load_dotenv()


@dataclass(frozen=True)
class Settings:
    openai_api_key: str
    script_model: str = "gpt-5.6-luna"
    tts_model: str = "gpt-4o-mini-tts"
    tts_voice: str = "alloy"
    video_width: int = 1080
    video_height: int = 1920
    video_fps: int = 30


def get_settings() -> Settings:
    api_key = os.getenv("OPENAI_API_KEY", "").strip()
    if not api_key:
        raise RuntimeError(
            "OPENAI_API_KEY não configurada. Copie .env.example para .env e informe a chave."
        )

    return Settings(
        openai_api_key=api_key,
        script_model=os.getenv("SCRIPT_MODEL", "gpt-5.6-luna"),
        tts_model=os.getenv("TTS_MODEL", "gpt-4o-mini-tts"),
        tts_voice=os.getenv("TTS_VOICE", "alloy"),
        video_width=int(os.getenv("VIDEO_WIDTH", "1080")),
        video_height=int(os.getenv("VIDEO_HEIGHT", "1920")),
        video_fps=int(os.getenv("VIDEO_FPS", "30")),
    )
