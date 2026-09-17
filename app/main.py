from __future__ import annotations

import argparse
from datetime import datetime
from pathlib import Path

from .config import get_settings
from .script_generator import generate_script
from .tts import concatenate_audio, synthesize_segments
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

    print(f"[1/4] Preparando roteiro: {args.topic}")
    script = generate_script(args.topic)

    print("[2/4] Gerando voz neural em português do Brasil")
    clips = synthesize_segments(
        texts=[segment.narration for segment in script.segments],
        out_dir=out_dir / "audio",
        model_path=Path(settings.tts_model),
    )
    narration_path = concatenate_audio(clips, out_dir / "narration.wav")

    print("[3/4] Montando vídeo, movimento e legendas")
    video_path = build_video(
        script=script,
        audio_path=narration_path,
        segment_durations=[clip.duration for clip in clips],
        out_dir=out_dir,
        width=settings.video_width,
        height=settings.video_height,
        fps=settings.video_fps,
    )

    print("[4/4] Pacote de publicação concluído")
    print(f"Vídeo: {video_path.resolve()}")
    print(f"Texto do post: {(out_dir / 'post.txt').resolve()}")
    print(f"Capa: {(out_dir / 'cover.jpg').resolve()}")


if __name__ == "__main__":
    main()
