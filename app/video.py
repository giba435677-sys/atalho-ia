from __future__ import annotations

import json
import math
import shutil
import subprocess
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

from .script_generator import VideoScript


PALETTES = [
    ((10, 16, 32), (32, 18, 68), (93, 70, 255)),
    ((8, 24, 30), (15, 55, 68), (21, 201, 176)),
    ((27, 12, 31), (68, 24, 63), (255, 85, 134)),
    ((24, 16, 8), (69, 42, 14), (255, 177, 63)),
    ((12, 18, 28), (30, 43, 66), (77, 166, 255)),
]


def ensure_ffmpeg() -> None:
    if not shutil.which("ffmpeg"):
        raise RuntimeError("FFmpeg não encontrado no PATH.")


def _font(size: int, bold: bool = False) -> ImageFont.FreeTypeFont | ImageFont.ImageFont:
    candidates = [
        "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf" if bold else "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
        "/usr/share/fonts/truetype/liberation2/LiberationSans-Bold.ttf" if bold else "/usr/share/fonts/truetype/liberation2/LiberationSans-Regular.ttf",
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


def _gradient(width: int, height: int, top: tuple[int, int, int], bottom: tuple[int, int, int]) -> Image.Image:
    img = Image.new("RGB", (width, height), top)
    draw = ImageDraw.Draw(img)
    for y in range(height):
        t = y / max(height - 1, 1)
        rgb = tuple(round(a + (b - a) * t) for a, b in zip(top, bottom))
        draw.line((0, y, width, y), fill=rgb)
    return img


def _rounded_text_box(
    draw: ImageDraw.ImageDraw,
    xy: tuple[int, int, int, int],
    fill: tuple[int, int, int],
    radius: int = 32,
) -> None:
    draw.rounded_rectangle(xy, radius=radius, fill=fill)


def create_scenes(script: VideoScript, out_dir: Path, width: int, height: int) -> list[Path]:
    scenes_dir = out_dir / "scenes"
    scenes_dir.mkdir(parents=True, exist_ok=True)

    brand_font = _font(38, bold=True)
    kicker_font = _font(34, bold=True)
    headline_font = _font(82, bold=True)
    number_font = _font(230, bold=True)
    footer_font = _font(30, bold=False)

    scene_paths: list[Path] = []
    for idx, segment in enumerate(script.segments, start=1):
        top, bottom, accent = PALETTES[(idx - 1) % len(PALETTES)]
        img = _gradient(width, height, top, bottom).convert("RGBA")
        draw = ImageDraw.Draw(img, "RGBA")

        # Decorative motion-design elements.
        r1 = 240 + (idx % 3) * 45
        draw.ellipse((width - r1, 120, width + 80, 120 + r1), fill=(*accent, 42))
        draw.ellipse((-180, height - 610, 420, height - 10), fill=(*accent, 26))
        for n in range(5):
            offset = 110 + n * 62
            draw.line((width - 360, offset, width - 60, offset + 145), fill=(*accent, 38), width=5)

        margin = 78
        _rounded_text_box(draw, (margin, 76, margin + 245, 142), (*accent, 235), radius=28)
        draw.text((margin + 22, 88), "ATALHO IA", font=brand_font, fill=(255, 255, 255, 255))
        draw.text((margin, 182), "PRODUTIVIDADE • AUTOMAÇÃO", font=kicker_font, fill=(222, 227, 239, 220))

        # Giant scene number in the background.
        scene_no = f"{idx:02d}"
        num_box = draw.textbbox((0, 0), scene_no, font=number_font)
        draw.text(
            (width - (num_box[2] - num_box[0]) - 70, 335),
            scene_no,
            font=number_font,
            fill=(255, 255, 255, 26),
        )

        # Main headline card.
        card_top = 650
        card_bottom = 1275
        draw.rounded_rectangle(
            (margin, card_top, width - margin, card_bottom),
            radius=54,
            fill=(8, 12, 24, 186),
            outline=(*accent, 165),
            width=4,
        )
        draw.rectangle((margin, card_top, margin + 14, card_bottom), fill=(*accent, 255))

        lines = _wrap(draw, segment.on_screen_text.upper(), headline_font, width - 2 * margin - 110)
        line_height = 108
        block_h = len(lines) * line_height
        y = card_top + (card_bottom - card_top - block_h) // 2
        for line in lines:
            draw.text((margin + 54, y), line, font=headline_font, fill=(255, 255, 255, 255))
            y += line_height

        # Bottom utility strip and progress.
        draw.text((margin, height - 235), "IDEIA PRÁTICA PARA USAR HOJE", font=kicker_font, fill=(230, 233, 243, 220))
        bar_y = height - 150
        bar_w = width - 2 * margin
        draw.rounded_rectangle((margin, bar_y, margin + bar_w, bar_y + 14), radius=7, fill=(255, 255, 255, 40))
        progress = bar_w * idx / len(script.segments)
        draw.rounded_rectangle((margin, bar_y, margin + progress, bar_y + 14), radius=7, fill=(*accent, 255))
        draw.text((width - margin - 150, height - 108), f"{idx}/{len(script.segments)}", font=footer_font, fill=(225, 229, 239, 190))

        path = scenes_dir / f"scene_{idx:03d}.png"
        img.convert("RGB").save(path, quality=96)
        scene_paths.append(path)

    # Cover for manual thumbnail selection.
    cover = Image.open(scene_paths[0]).convert("RGB")
    cover.save(out_dir / "cover.jpg", quality=94)
    return scene_paths


def _ass_time(seconds: float) -> str:
    seconds = max(0.0, seconds)
    h = int(seconds // 3600)
    m = int((seconds % 3600) // 60)
    s = seconds % 60
    return f"{h}:{m:02d}:{s:05.2f}"


def _srt_time(seconds: float) -> str:
    ms = max(0, round(seconds * 1000))
    h, rem = divmod(ms, 3_600_000)
    m, rem = divmod(rem, 60_000)
    s, ms = divmod(rem, 1000)
    return f"{h:02d}:{m:02d}:{s:02d},{ms:03d}"


def _caption_chunks(text: str, words_per_chunk: int = 5) -> list[str]:
    words = text.split()
    chunks = [" ".join(words[i : i + words_per_chunk]) for i in range(0, len(words), words_per_chunk)]
    return chunks or [text]


def create_captions(script: VideoScript, durations: list[float], out_dir: Path) -> tuple[Path, Path]:
    if len(script.segments) != len(durations):
        raise ValueError("Quantidade de trechos e durações não corresponde.")

    ass_path = out_dir / "captions.ass"
    srt_path = out_dir / "captions.srt"

    ass_lines = [
        "[Script Info]",
        "ScriptType: v4.00+",
        "PlayResX: 1080",
        "PlayResY: 1920",
        "WrapStyle: 2",
        "ScaledBorderAndShadow: yes",
        "",
        "[V4+ Styles]",
        "Format: Name,Fontname,Fontsize,PrimaryColour,SecondaryColour,OutlineColour,BackColour,Bold,Italic,Underline,StrikeOut,ScaleX,ScaleY,Spacing,Angle,BorderStyle,Outline,Shadow,Alignment,MarginL,MarginR,MarginV,Encoding",
        "Style: Caption,DejaVu Sans,55,&H00FFFFFF,&H00FFFFFF,&H00101010,&H9A050505,-1,0,0,0,100,100,0,0,3,2,0,2,80,80,225,1",
        "",
        "[Events]",
        "Format: Layer,Start,End,Style,Name,MarginL,MarginR,MarginV,Effect,Text",
    ]
    srt_blocks: list[str] = []
    current = 0.0
    srt_idx = 1

    for segment, duration in zip(script.segments, durations):
        chunks = _caption_chunks(segment.narration, words_per_chunk=5)
        words_total = sum(max(1, len(c.split())) for c in chunks)
        local = 0.0
        for chunk in chunks:
            weight = max(1, len(chunk.split())) / words_total
            chunk_duration = duration * weight
            start = current + local
            end = min(current + duration, start + chunk_duration)
            safe_chunk = chunk.replace("{", "(").replace("}", ")")
            ass_lines.append(
                f"Dialogue: 0,{_ass_time(start)},{_ass_time(end)},Caption,,0,0,0,,{{\\fad(70,70)}}{safe_chunk}"
            )
            srt_blocks.append(
                f"{srt_idx}\n{_srt_time(start)} --> {_srt_time(end)}\n{chunk}\n"
            )
            srt_idx += 1
            local += chunk_duration
        current += duration

    ass_path.write_text("\n".join(ass_lines) + "\n", encoding="utf-8")
    srt_path.write_text("\n".join(srt_blocks), encoding="utf-8")
    return ass_path, srt_path


def _write_publication_files(script: VideoScript, durations: list[float], out_dir: Path) -> None:
    total_seconds = sum(durations)
    metadata = {
        "title": script.title,
        "description": script.description,
        "hashtags": script.hashtags,
        "duration_seconds": round(total_seconds, 2),
        "format": "1080x1920 / H.264 / AAC",
        "segments": [
            {
                "narration": segment.narration,
                "on_screen_text": segment.on_screen_text,
                "duration_seconds": round(duration, 2),
            }
            for segment, duration in zip(script.segments, durations)
        ],
    }
    (out_dir / "metadata.json").write_text(
        json.dumps(metadata, ensure_ascii=False, indent=2), encoding="utf-8"
    )

    hashtags = " ".join(script.hashtags)
    post = f"{script.title}\n\n{script.description}\n\n{hashtags}\n"
    (out_dir / "post.txt").write_text(post, encoding="utf-8")


def build_video(
    script: VideoScript,
    audio_path: Path,
    segment_durations: list[float],
    out_dir: Path,
    width: int,
    height: int,
    fps: int,
) -> Path:
    ensure_ffmpeg()
    if not segment_durations or any(d <= 0 for d in segment_durations):
        raise ValueError("Durações de áudio inválidas.")

    scenes = create_scenes(script, out_dir, width, height)
    ass_path, _ = create_captions(script, segment_durations, out_dir)
    _write_publication_files(script, segment_durations, out_dir)

    concat_path = out_dir / "scenes.txt"
    with concat_path.open("w", encoding="utf-8") as f:
        for scene, duration in zip(scenes, segment_durations):
            safe = scene.resolve().as_posix().replace("'", "'\\''")
            f.write(f"file '{safe}'\n")
            f.write(f"duration {duration:.4f}\n")
        safe = scenes[-1].resolve().as_posix().replace("'", "'\\''")
        f.write(f"file '{safe}'\n")

    total_duration = sum(segment_durations)
    output_path = out_dir / "video_publish.mp4"
    ass_filter_path = ass_path.as_posix().replace("\\", "/").replace(":", "\\:")

    filter_chain = (
        f"fps={fps},"
        f"scale={width + 80}:{height + 142},"
        f"crop={width}:{height}:"
        "x='(iw-ow)/2+18*sin(t*0.55)':"
        "y='(ih-oh)/2+22*cos(t*0.41)',"
        f"ass='{ass_filter_path}'"
    )

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
        filter_chain,
        "-af",
        "loudnorm=I=-16:TP=-1.5:LRA=11",
        "-t",
        f"{total_duration:.3f}",
        "-c:v",
        "libx264",
        "-preset",
        "medium",
        "-crf",
        "20",
        "-pix_fmt",
        "yuv420p",
        "-c:a",
        "aac",
        "-b:a",
        "192k",
        "-ar",
        "44100",
        "-movflags",
        "+faststart",
        "-metadata",
        f"title={script.title}",
        str(output_path),
    ]

    result = subprocess.run(cmd, capture_output=True, text=True)
    if result.returncode != 0:
        raise RuntimeError(f"FFmpeg falhou:\n{result.stderr[-5000:]}")

    return output_path
