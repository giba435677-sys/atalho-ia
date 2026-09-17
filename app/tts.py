from __future__ import annotations

import shutil
import subprocess
from dataclasses import dataclass
from pathlib import Path


@dataclass
class AudioClip:
    path: Path
    duration: float


def _probe_duration(path: Path) -> float:
    if not shutil.which("ffprobe"):
        raise RuntimeError("ffprobe não encontrado no PATH.")
    result = subprocess.run(
        [
            "ffprobe",
            "-v",
            "error",
            "-show_entries",
            "format=duration",
            "-of",
            "default=noprint_wrappers=1:nokey=1",
            str(path),
        ],
        capture_output=True,
        text=True,
    )
    if result.returncode != 0:
        raise RuntimeError(f"ffprobe falhou: {result.stderr.strip()}")
    return float(result.stdout.strip())


def synthesize_segments(texts: list[str], out_dir: Path, model_path: Path) -> list[AudioClip]:
    if not shutil.which("piper"):
        raise RuntimeError("Piper TTS não encontrado no PATH.")
    if not model_path.exists():
        raise RuntimeError(f"Modelo de voz não encontrado: {model_path}")

    out_dir.mkdir(parents=True, exist_ok=True)
    clips: list[AudioClip] = []

    for idx, text in enumerate(texts, start=1):
        output_path = out_dir / f"voice_{idx:03d}.wav"
        result = subprocess.run(
            [
                "piper",
                "--model",
                str(model_path),
                "--output_file",
                str(output_path),
            ],
            input=text.strip() + "\n",
            capture_output=True,
            text=True,
        )
        if result.returncode != 0:
            raise RuntimeError(f"Piper falhou no trecho {idx}: {result.stderr.strip()}")
        clips.append(AudioClip(path=output_path, duration=_probe_duration(output_path)))

    return clips


def concatenate_audio(clips: list[AudioClip], output_path: Path) -> Path:
    if not clips:
        raise ValueError("Nenhum áudio para concatenar.")
    if not shutil.which("ffmpeg"):
        raise RuntimeError("FFmpeg não encontrado no PATH.")

    output_path.parent.mkdir(parents=True, exist_ok=True)
    concat_file = output_path.parent / "audio_concat.txt"
    with concat_file.open("w", encoding="utf-8") as f:
        for clip in clips:
            safe = clip.path.resolve().as_posix().replace("'", "'\\''")
            f.write(f"file '{safe}'\n")

    result = subprocess.run(
        [
            "ffmpeg",
            "-y",
            "-f",
            "concat",
            "-safe",
            "0",
            "-i",
            str(concat_file),
            "-ar",
            "44100",
            "-ac",
            "2",
            "-c:a",
            "pcm_s16le",
            str(output_path),
        ],
        capture_output=True,
        text=True,
    )
    if result.returncode != 0:
        raise RuntimeError(f"FFmpeg falhou ao unir narração: {result.stderr[-2500:]}")
    return output_path
