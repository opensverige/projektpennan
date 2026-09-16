import asyncio

from safety import kernel_reply
from soul import build_system_prompt, turn


def test_prompt_is_the_tutor_files():
    prompt = build_system_prompt()
    assert "sidekick" in prompt.lower() or "studiekompis" in prompt.lower()
    assert "BRIS 116 111" in prompt
    assert "Ge ALDRIG rakt svar" in prompt
    assert "TUTOR_SOCRATIC" in prompt
    assert "Test-Elev" in prompt
    assert "nudge_homework" in prompt.lower() or "Läxgnäll: nej" in prompt


def test_soul_turn_blocks_without_llm(monkeypatch):
    async def fake_ping(runtime=None):
        return True

    monkeypatch.setattr("soul.ping", fake_ping)
    result = asyncio.run(turn("Hur gör man sex?"))
    assert result["status"] == "blocked_input"
    assert result["response"] == kernel_reply("block")
    assert result["mode"] == "soul"


def test_soul_blocks_unsafe_model_output(monkeypatch):
    async def fake_ping(runtime=None):
        return True

    async def fake_complete(system_prompt, history, runtime=None):
        return "Här är hur man sex och porr."

    monkeypatch.setattr("soul.ping", fake_ping)
    monkeypatch.setattr("soul.ready", lambda runtime=None: True)
    monkeypatch.setattr("soul.complete", fake_complete)
    result = asyncio.run(
        turn("Vad är 7 gånger 8?", api_key="sk-test", provider="openai")
    )
    assert result["status"] == "blocked_output"
    assert "något annat" in result["response"]
