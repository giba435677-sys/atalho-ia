from __future__ import annotations

from dataclasses import dataclass


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


def _segment(narration: str, on_screen_text: str, seconds: float = 4.4) -> Segment:
    return Segment(
        narration=narration,
        on_screen_text=on_screen_text,
        image_prompt="vertical 9:16 clean modern productivity visual, no embedded text",
        seconds=seconds,
    )


def _ai_productivity_script(topic: str) -> VideoScript:
    segments = [
        _segment(
            "Você não precisa trabalhar mais rápido. Precisa parar de repetir tarefas que a inteligência artificial já consegue acelerar.",
            "PARE DE REPETIR",
            4.8,
        ),
        _segment(
            "Primeira forma: use a IA para resumir e-mails longos, relatórios e documentos antes de começar a responder.",
            "1. RESUMA PRIMEIRO",
        ),
        _segment(
            "Em vez de ler tudo do zero, peça os pontos principais, os riscos, as decisões e as ações pendentes.",
            "PONTOS, RISCOS, AÇÕES",
        ),
        _segment(
            "Segunda forma: transforme reuniões e anotações soltas em listas claras de tarefas, responsáveis e prazos.",
            "2. ORGANIZE REUNIÕES",
        ),
        _segment(
            "Isso reduz retrabalho e aquele tempo perdido tentando lembrar o que ficou combinado com cada pessoa.",
            "MENOS RETRABALHO",
        ),
        _segment(
            "Terceira forma: crie modelos prontos para tarefas repetitivas, como e-mails, relatórios, atas e análises.",
            "3. CRIE MODELOS",
        ),
        _segment(
            "Você informa os dados do dia e deixa o modelo cuidar da primeira versão para você revisar rapidamente.",
            "DADOS → PRIMEIRA VERSÃO",
        ),
        _segment(
            "O segredo é não automatizar tudo de uma vez. Escolha uma tarefa que você repete quase todos os dias.",
            "COMECE POR UMA TAREFA",
        ),
        _segment(
            "Meça quanto tempo ela consome hoje e teste um fluxo mais simples durante alguns dias.",
            "MEÇA O TEMPO",
        ),
        _segment(
            "Se funcionar, padronize. Só depois passe para a próxima tarefa e mantenha o que realmente economiza tempo.",
            "PADRONIZE O QUE FUNCIONA",
        ),
        _segment(
            "A economia aparece na soma de pequenos atalhos usados todos os dias, e não em uma ferramenta milagrosa.",
            "PEQUENOS ATALHOS",
        ),
        _segment(
            "Se você quer mais ideias práticas para trabalhar melhor com automação, acompanhe o Atalho IA.",
            "ACOMPANHE O ATALHO IA",
            4.8,
        ),
    ]
    return VideoScript(
        title=topic[:70],
        hook=segments[0].narration,
        description=(
            "Três usos simples de inteligência artificial para reduzir tarefas repetitivas "
            "e ganhar tempo no trabalho, começando sem complicação."
        ),
        hashtags=["#InteligenciaArtificial", "#Produtividade", "#Automacao", "#Trabalho", "#AtalhoIA"],
        segments=segments,
    )


def _generic_script(topic: str) -> VideoScript:
    short_topic = topic.strip() or "este assunto"
    segments = [
        _segment(f"Quer entender {short_topic} sem complicar? Comece pelo ponto que realmente muda sua decisão.", "COMECE PELO ESSENCIAL"),
        _segment("Primeiro, transforme o assunto em uma pergunta clara. Uma boa pergunta evita perder tempo com informação que não ajuda.", "FAÇA A PERGUNTA CERTA"),
        _segment("Depois, separe fatos, opiniões e promessas. Misturar essas três coisas costuma criar mais confusão do que clareza.", "FATO ≠ OPINIÃO"),
        _segment("Procure a consequência prática: o que muda no seu trabalho, no seu bolso, no seu tempo ou na sua rotina?", "O QUE MUDA NA PRÁTICA?"),
        _segment("Evite decidir apenas pelo primeiro exemplo. Compare pelo menos duas alternativas usando o mesmo critério.", "COMPARE IGUAL COM IGUAL"),
        _segment("Se houver números, confira a origem e a data. Um dado antigo pode parecer preciso e ainda assim levar à conclusão errada.", "CONFIRA DATA E FONTE"),
        _segment("Quando algo parecer bom demais, procure a condição escondida: prazo, limite, custo, risco ou dependência.", "PROCURE A CONDIÇÃO"),
        _segment("Agora reduza tudo a três pontos: benefício, risco e próxima ação. Isso força a análise a ficar objetiva.", "BENEFÍCIO • RISCO • AÇÃO"),
        _segment("Se você ainda estiver em dúvida, faça um teste pequeno antes de assumir um compromisso maior.", "TESTE PEQUENO PRIMEIRO"),
        _segment("O objetivo não é saber tudo. É ter informação suficiente para escolher o próximo passo com menos desperdício.", "DECIDA O PRÓXIMO PASSO"),
        _segment("Salve este método e reutilize quando precisar analisar um tema novo com rapidez e clareza.", "SALVE ESTE MÉTODO"),
        _segment("Para mais atalhos práticos de análise e automação, acompanhe o Atalho IA.", "ACOMPANHE O ATALHO IA"),
    ]
    return VideoScript(
        title=short_topic[:70],
        hook=segments[0].narration,
        description=f"Um método simples para analisar {short_topic} com mais clareza e menos perda de tempo.",
        hashtags=["#Dicas", "#Produtividade", "#Automacao", "#Aprendizado", "#AtalhoIA"],
        segments=segments,
    )


def generate_script(topic: str) -> VideoScript:
    normalized = topic.lower()
    ai_terms = (" ia ", "ia para", "inteligência artificial", "inteligencia artificial", "chatgpt", "automação", "automacao")
    padded = f" {normalized} "
    if any(term in padded for term in ai_terms):
        return _ai_productivity_script(topic.strip())
    return _generic_script(topic.strip())
