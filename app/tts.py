from __future__ import annotations

import shutil
import subprocess
from pathlib import Path


def synthesize_speech(
    text: str,
    output_path: Path,
    voice: str = "pt-br",
    speed: int = 165,
    pitch: int = 48,
) -> Path:
    if not shutil.which("espeak-ng"):
        raise RuntimeError("espeak-ng não encontrado no PATH.")

    output_path = output_path.with_suffix(".wav")
    output_path.parent.mkdir(parents=True, exist_ok=True)

    cmd = [
        "espeak-ng",
        "-v",
        voice,
        "-s",
        str(speed),
        "-p",
        str(pitch),
        "-w",
        str(output_path),
        text,
    ]
    result = subprocess.run(cmd, capture_output=True, text=True)
    if result.returncode != 0:
        raise RuntimeError(f"espeak-ng falhou: {result.stderr.strip()}")

    return output_path
