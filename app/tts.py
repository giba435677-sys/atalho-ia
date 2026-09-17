from __future__ import annotations

from pathlib import Path

from openai import OpenAI


def synthesize_speech(
    client: OpenAI,
    text: str,
    output_path: Path,
    model: str,
    voice: str,
) -> Path:
    output_path.parent.mkdir(parents=True, exist_ok=True)

    with client.audio.speech.with_streaming_response.create(
        model=model,
        voice=voice,
        input=text,
        instructions=(
            "Fale em português do Brasil, com energia, clareza e ritmo de vídeo curto. "
            "Evite tom de locutor artificial. Faça pequenas pausas naturais."
        ),
    ) as response:
        response.stream_to_file(output_path)

    return output_path
