from __future__ import annotations

import argparse
from datetime import datetime
from pathlib import Path

from .config import get_settings
from .script_generator import generate_script
from .tts import synthesize_speech
from .video import build_video


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Atalho IA - gerador gratuito de vídeos curtos")
    parser.add_argument("--topic", required=True, help="Tema do vídeo")
    parser.add_argument("--output", default="output", help="Diretório base de saída")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    settings = get_settings()

    stamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    out_dir = Path(args.output) / stamp
    out_dir.mkdir(parents=True, exist_ok=True)

    print(f"[1/3] Gerando roteiro local: {args.topic}")
    script = generate_script(args.topic)

    print("[2/3] Gerando narração local")
    audio_path = synthesize_speech(
        text=script.narration,
        output_path=out_dir / "narration.wav",
        voice=settings.tts_voice,
        speed=settings.tts_speed,
        pitch=settings.tts_pitch,
    )

    print("[3/3] Montando vídeo")
    video_path = build_video(
        script=script,
        audio_path=audio_path,
        out_dir=out_dir,
        width=settings.video_width,
        height=settings.video_height,
        fps=settings.video_fps,
    )

    print(f"Concluído: {video_path.resolve()}")


if __name__ == "__main__":
    main()
