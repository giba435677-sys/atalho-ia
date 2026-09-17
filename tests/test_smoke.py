from app.script_generator import Segment, VideoScript


def test_narration_join():
    script = VideoScript(
        title="Teste",
        hook="Gancho",
        description="Descrição",
        hashtags=["#teste"],
        segments=[
            Segment("Primeira frase.", "PRIMEIRA", "prompt 1", 4.0),
            Segment("Segunda frase.", "SEGUNDA", "prompt 2", 4.0),
        ],
    )
    assert script.narration == "Primeira frase. Segunda frase."
