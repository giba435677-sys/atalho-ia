# Atalho IA

MVP de automação para gerar vídeos verticais curtos (Shorts/Reels/TikTok) com o menor custo possível e pouca intervenção manual.

## O que esta primeira versão faz

1. Recebe um tema.
2. Gera roteiro de 45–60 segundos em JSON.
3. Gera uma narração com OpenAI TTS.
4. Cria cartões verticais para cada trecho do roteiro sem pagar por imagens.
5. Monta o vídeo 1080x1920 com FFmpeg.
6. Salva roteiro, áudio, imagens e MP4 em `output/`.

A publicação automática e a busca de imagens/B-roll entram depois que este núcleo estiver validado.

## Requisitos

- Python 3.11+
- FFmpeg instalado e disponível no PATH
- `OPENAI_API_KEY`

## Instalação

```bash
python -m venv .venv
```

Windows:

```powershell
.venv\Scripts\activate
pip install -r requirements.txt
copy .env.example .env
```

Linux/macOS:

```bash
source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
```

Edite o arquivo `.env` e coloque sua chave.

## Executar

```bash
python -m app.main --topic "História da Roma Antiga"
```

O vídeo será criado em `output/<data-hora>/video.mp4`.

## Modelos padrão

- Roteiro: `gpt-5.6-luna`, priorizando baixo custo.
- Voz: `gpt-4o-mini-tts`.

Os dois podem ser alterados no `.env`.

## Estrutura

```text
app/
  config.py
  main.py
  script_generator.py
  tts.py
  video.py
.github/workflows/
  generate.yml
.env.example
.gitignore
Dockerfile
requirements.txt
```

## Automação no GitHub Actions

O workflow `generate.yml` permite disparar a geração manualmente no GitHub Actions informando um tema. Para funcionar, cadastre `OPENAI_API_KEY` em:

`Settings > Secrets and variables > Actions > New repository secret`

Nesta fase, o workflow não publica em redes sociais e não possui cron automático por padrão para evitar consumo inesperado de API.

## Próxima fase

- puxar imagens/B-roll gratuitos;
- inserir legendas dinâmicas;
- gerar títulos, descrição e hashtags;
- publicar automaticamente no YouTube Shorts;
- escolher temas automaticamente;
- registrar visualizações e aprender quais temas performam melhor.
