from __future__ import annotations

from dataclasses import dataclass


@dataclass
class Segment:
    narration: str
    on_screen_text: str
    image_prompt: str
    seconds: float = 0.0


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


def _segment(narration: str, on_screen_text: str) -> Segment:
    return Segment(
        narration=narration,
        on_screen_text=on_screen_text,
        image_prompt="original abstract vertical motion graphic, no stock media, no embedded text",
    )


def _ai_productivity_script() -> VideoScript:
    segments = [
        _segment(
            "Se você usa inteligência artificial só para fazer perguntas, provavelmente está deixando tempo na mesa.",
            "VOCÊ ESTÁ PERDENDO TEMPO",
        ),
        _segment(
            "Primeiro: jogue e-mails, relatórios e documentos longos nela e peça quatro coisas: resumo, riscos, decisões e pendências.",
            "1 • RESUMA ANTES DE LER TUDO",
        ),
        _segment(
            "Você para de caçar informação e começa por aquilo que realmente exige sua atenção.",
            "FOQUE NO QUE EXIGE DECISÃO",
        ),
        _segment(
            "Segundo: depois de uma reunião, transforme as anotações em tarefas, responsáveis e prazos.",
            "2 • SAIA COM AÇÕES CLARAS",
        ),
        _segment(
            "Isso reduz o clássico quem ficou de fazer o quê e corta muito retrabalho.",
            "MENOS DÚVIDA • MENOS RETRABALHO",
        ),
        _segment(
            "Terceiro: crie modelos para e-mails, atas, relatórios e análises que você repete toda semana.",
            "3 • CRIE MODELOS REUTILIZÁVEIS",
        ),
        _segment(
            "No dia a dia, você só troca os dados e revisa a primeira versão.",
            "TROQUE OS DADOS • REVISE",
        ),
        _segment(
            "Não tente automatizar tudo. Escolha uma tarefa repetitiva e teste por uma semana.",
            "COMECE PEQUENO",
        ),
        _segment(
            "Se economizar tempo e mantiver qualidade, padronize. Depois passe para a próxima.",
            "FUNCIONOU? PADRONIZE",
        ),
        _segment(
            "Pequenos atalhos viram horas no mês. Salve este vídeo e acompanhe o Atalho IA.",
            "SALVE • TESTE • ACOMPANHE",
        ),
    ]
    return VideoScript(
        title="3 jeitos de usar IA para ganhar tempo no trabalho",
        hook=segments[0].narration,
        description=(
            "Três usos práticos de inteligência artificial para reduzir tarefas repetitivas, "
            "organizar melhor o trabalho e ganhar tempo sem complicar a rotina."
        ),
        hashtags=["#InteligenciaArtificial", "#Produtividade", "#Automacao", "#Trabalho", "#AtalhoIA"],
        segments=segments,
    )


def _generic_script(topic: str) -> VideoScript:
    short_topic = topic.strip() or "este assunto"
    segments = [
        _segment(f"Quer entender {short_topic} sem complicar? Comece pelo que realmente muda sua decisão.", "COMECE PELO ESSENCIAL"),
        _segment("Transforme o assunto em uma pergunta clara. Isso elimina muita informação que parece útil, mas não ajuda.", "FAÇA A PERGUNTA CERTA"),
        _segment("Separe fatos, opiniões e promessas. Misturar essas três coisas costuma criar mais confusão do que clareza.", "FATO NÃO É OPINIÃO"),
        _segment("Procure a consequência prática: o que muda no seu tempo, no seu dinheiro ou na sua rotina?", "O QUE MUDA NA PRÁTICA?"),
        _segment("Compare alternativas usando o mesmo critério e não apenas o primeiro exemplo que apareceu.", "COMPARE IGUAL COM IGUAL"),
        _segment("Quando houver números, confira a origem e a data. Dado antigo também pode enganar.", "CONFIRA DATA E FONTE"),
        _segment("Agora reduza tudo a três pontos: benefício, risco e próxima ação.", "BENEFÍCIO • RISCO • AÇÃO"),
        _segment("Se ainda houver dúvida, faça um teste pequeno antes de assumir um compromisso maior.", "TESTE PEQUENO PRIMEIRO"),
        _segment("O objetivo não é saber tudo. É escolher o próximo passo com menos desperdício.", "DECIDA O PRÓXIMO PASSO"),
        _segment("Salve este método e acompanhe o Atalho IA para mais ideias práticas.", "SALVE • ACOMPANHE"),
    ]
    return VideoScript(
        title=short_topic[:70],
        hook=segments[0].narration,
        description=f"Um método direto para analisar {short_topic} com mais clareza e menos perda de tempo.",
        hashtags=["#Dicas", "#Produtividade", "#Automacao", "#Aprendizado", "#AtalhoIA"],
        segments=segments,
    )


def generate_script(topic: str) -> VideoScript:
    normalized = f" {topic.lower()} "
    ai_terms = (" ia ", "ia para", "inteligência artificial", "inteligencia artificial", "chatgpt", "automação", "automacao")
    if any(term in normalized for term in ai_terms):
        return _ai_productivity_script()
    return _generic_script(topic)
