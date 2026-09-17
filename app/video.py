from __future__ import annotations

import json
import shutil
import subprocess
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

from .script_generator import VideoScript


def ensure_ffmpeg() -> None:
    if not shutil.which("ffmpeg"):
        raise RuntimeError("FFmpeg não encontrado no PATH.")


def _font(size: int, bold: bool = False) -> ImageFont.FreeTypeFont | ImageFont.ImageFont:
    candidates = [
        "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf" if bold else "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
        "C:/Windows/Fonts/arialbd.ttf" if bold else "C:/Windows/Fonts/arial.ttf",
        "/System/Library/Fonts/Supplemental/Arial Bold.ttf" if bold else "/System/Library/Fonts/Supplemental/Arial.ttf",
    ]
    for candidate in candidates:
        try:
            return ImageFont.truetype(candidate, size=size)
        except OSError:
            continue
    return ImageFont.load_default()


def _wrap(draw: ImageDraw.ImageDraw, text: str, font, max_width: int) -> list[str]:
    words = text.split()
    lines: list[str] = []
    current = ""
    for word in words:
        candidate = f"{current} {word}".strip()
        box = draw.textbbox((0, 0), candidate, font=font)
        if box[2] - box[0] <= max_width:
            current = candidate
        else:
            if current:
                lines.append(current)
            current = word
    if current:
        lines.append(current)
    return lines


def create_cards(script: VideoScript, out_dir: Path, width: int, height: int) -> list[Path]:
    cards_dir = out_dir / "cards"
    cards_dir.mkdir(parents=True, exist_ok=True)

    title_font = _font(64, bold=True)
    body_font = _font(92, bold=True)
    small_font = _font(38, bold=False)

    paths: list[Path] = []
    for idx, segment in enumerate(script.segments, start=1):
        img = Image.new("RGB", (width, height), (17, 19, 24))
        draw = ImageDraw.Draw(img)

        draw.rectangle((0, 0, width, int(height * 0.18)), fill=(28, 32, 41))
        draw.rectangle((0, int(height * 0.82), width, height), fill=(24, 27, 34))

        margin = int(width * 0.08)
        draw.text((margin, 90), script.title[:55], font=title_font, fill=(230, 234, 242))

        lines = _wrap(draw, segment.on_screen_text.upper(), body_font, width - 2 * margin)
        line_height = 118
        block_height = max(1, len(lines)) * line_height
        y = (height - block_height) // 2
        for line in lines:
            box = draw.textbbox((0, 0), line, font=body_font)
            x = (width - (box[2] - box[0])) // 2
            draw.text((x, y), line, font=body_font, fill=(255, 255, 255))
            y += line_height

        footer = f"{idx:02d}/{len(script.segments):02d}"
        draw.text((margin, height - 120), footer, font=small_font, fill=(180, 185, 196))

        path = cards_dir / f"card_{idx:03d}.png"
        img.save(path, quality=95)
        paths.append(path)

    return paths


def build_video(
    script: VideoScript,
    audio_path: Path,
    out_dir: Path,
    width: int,
    height: int,
    fps: int,
) -> Path:
    ensure_ffmpeg()
    cards = create_cards(script, out_dir, width, height)

    concat_path = out_dir / "frames.txt"
    with concat_path.open("w", encoding="utf-8") as f:
        for card, segment in zip(cards, script.segments):
            safe = card.resolve().as_posix().replace("'", "'\\''")
            f.write(f"file '{safe}'\n")
            f.write(f"duration {segment.seconds:.3f}\n")
        safe = cards[-1].resolve().as_posix().replace("'", "'\\''")
        f.write(f"file '{safe}'\n")

    output_path = out_dir / "video.mp4"
    cmd = [
        "ffmpeg",
        "-y",
        "-f",
        "concat",
        "-safe",
        "0",
        "-i",
        str(concat_path),
        "-i",
        str(audio_path),
        "-vf",
        f"fps={fps},scale={width}:{height}:force_original_aspect_ratio=decrease,pad={width}:{height}:(ow-iw)/2:(oh-ih)/2",
        "-c:v",
        "libx264",
        "-pix_fmt",
        "yuv420p",
        "-c:a",
        "aac",
        "-b:a",
        "192k",
        "-shortest",
        "-movflags",
        "+faststart",
        str(output_path),
    ]

    result = subprocess.run(cmd, capture_output=True, text=True)
    if result.returncode != 0:
        raise RuntimeError(f"FFmpeg falhou:\n{result.stderr[-4000:]}")

    metadata = {
        "title": script.title,
        "description": script.description,
        "hashtags": script.hashtags,
        "segments": [segment.__dict__ for segment in script.segments],
    }
    (out_dir / "script.json").write_text(
        json.dumps(metadata, ensure_ascii=False, indent=2), encoding="utf-8"
    )

    return output_path
