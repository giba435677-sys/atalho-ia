from __future__ import annotations

import argparse
from datetime import datetime
from pathlib import Path

from openai import OpenAI

from .config import get_settings
from .script_generator import generate_script
from .tts import synthesize_speech
from .video import build_video


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Atalho IA - gerador de vídeos curtos")
    parser.add_argument("--topic", required=True, help="Tema do vídeo")
    parser.add_argument("--output", default="output", help="Diretório base de saída")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    settings = get_settings()
    client = OpenAI(api_key=settings.openai_api_key)

    stamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    out_dir = Path(args.output) / stamp
    out_dir.mkdir(parents=True, exist_ok=True)

    print(f"[1/3] Gerando roteiro: {args.topic}")
    script = generate_script(client, args.topic, settings.script_model)

    print("[2/3] Gerando narração")
    audio_path = synthesize_speech(
        client=client,
        text=script.narration,
        output_path=out_dir / "narration.mp3",
        model=settings.tts_model,
        voice=settings.tts_voice,
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
