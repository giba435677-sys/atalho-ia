# Atalho IA

MVP de automação para gerar vídeos verticais curtos (Shorts/Reels/TikTok) com pouca intervenção manual e sem depender de API paga.

## O que esta versão faz

1. Recebe um tema.
2. Gera um roteiro local estruturado para vídeo curto.
3. Gera narração local em português com `espeak-ng`.
4. Cria cartões verticais para cada trecho do roteiro.
5. Monta o vídeo 1080x1920 com FFmpeg.
6. Salva roteiro, áudio, imagens e MP4 em `output/`.
7. No GitHub Actions, empacota tudo em um artefato para download.

A publicação automática e a melhoria visual entram nas próximas fases.

## Custo desta fase

Esta versão não usa OpenAI API, ElevenLabs ou outro serviço pago de IA. O núcleo roda com ferramentas locais e GitHub Actions.

## Requisitos locais

- Python 3.11+
- FFmpeg
- espeak-ng

## Instalação

```bash
python -m venv .venv
```

Windows:

```powershell
.venv\Scripts\activate
pip install -r requirements.txt
```

Linux/macOS:

```bash
source .venv/bin/activate
pip install -r requirements.txt
```

## Executar

```bash
python -m app.main --topic "3 formas práticas de usar IA para economizar tempo no trabalho"
```

O vídeo será criado em `output/<data-hora>/video.mp4`.

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

Abra a aba `Actions`, escolha `Generate short video`, clique em `Run workflow` e informe o tema. Nenhuma chave de API é necessária nesta versão.

O resultado fica disponível como artefato chamado `atalho-ia-output`.

## Limitação atual

Para zerar o custo, a primeira versão usa roteiro baseado em estruturas locais e uma voz sintética local. Isso valida o fluxo completo sem cobrança. Depois podemos melhorar a qualidade com modelos locais/open-source e B-roll gratuito sem voltar a depender de cartão.

## Próxima fase

- melhorar a voz sem API paga;
- adicionar imagens/B-roll gratuitos;
- inserir legendas dinâmicas;
- variar automaticamente os roteiros;
- gerar títulos, descrições e hashtags em lote;
- publicar automaticamente no YouTube Shorts;
- escolher temas automaticamente;
- registrar visualizações e aprender quais formatos performam melhor.
