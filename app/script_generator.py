from __future__ import annotations

import json
import re
from dataclasses import dataclass

from openai import OpenAI


@dataclass
class Segment:
    narration: str
    on_screen_text: str
    image_prompt: str
    seconds: float


@dataclass
class VideoScript:
    title: str
    hook: str
    description: str
    hashtags: list[str]
    segments: list[Segment]

    @property
    def narration(self) -> str:
        return " ".join(s.narration.strip() for s in self.segments if s.narration.strip())


def _extract_json(text: str) -> dict:
    text = text.strip()
    text = re.sub(r"^```(?:json)?\s*", "", text, flags=re.IGNORECASE)
    text = re.sub(r"\s*```$", "", text)
    return json.loads(text)


def generate_script(client: OpenAI, topic: str, model: str) -> VideoScript:
    prompt = f"""
Você é roteirista de vídeos verticais de alta retenção.
Crie um roteiro em português do Brasil sobre: {topic}

Regras:
- duração total entre 45 e 60 segundos;
- gancho forte nos primeiros 3 segundos;
- linguagem simples, direta e natural;
- sem inventar fatos; quando o tema exigir precisão, use formulações prudentes;
- 10 a 14 segmentos;
- cada segmento deve durar aproximadamente 3,5 a 5 segundos;
- texto na tela curto, com no máximo 8 palavras;
- image_prompt em inglês, descrevendo uma imagem vertical 9:16 cinematográfica, sem texto embutido;
- título curto e chamativo, sem sensacionalismo falso;
- descrição curta;
- 5 hashtags relevantes.

Retorne SOMENTE JSON válido neste formato:
{{
  "title": "...",
  "hook": "...",
  "description": "...",
  "hashtags": ["#..."],
  "segments": [
    {{
      "narration": "...",
      "on_screen_text": "...",
      "image_prompt": "...",
      "seconds": 4.0
    }}
  ]
}}
""".strip()

    response = client.responses.create(model=model, input=prompt)
    data = _extract_json(response.output_text)

    segments = [
        Segment(
            narration=str(item["narration"]),
            on_screen_text=str(item["on_screen_text"]),
            image_prompt=str(item["image_prompt"]),
            seconds=max(2.5, min(float(item.get("seconds", 4.0)), 6.0)),
        )
        for item in data["segments"]
    ]

    if not segments:
        raise ValueError("A IA não retornou segmentos para o vídeo.")

    return VideoScript(
        title=str(data["title"]),
        hook=str(data.get("hook", "")),
        description=str(data.get("description", "")),
        hashtags=[str(x) for x in data.get("hashtags", [])],
        segments=segments,
    )
