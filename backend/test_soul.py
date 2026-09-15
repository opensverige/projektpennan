from soul import build_system_prompt


def test_prompt_is_the_tutor_files():
    prompt = build_system_prompt()
    assert "sidekick" in prompt.lower() or "studiekompis" in prompt.lower()
    assert "BRIS 116 111" in prompt
    assert "Ge ALDRIG rakt svar" in prompt
    assert "TUTOR_SOCRATIC" in prompt
    assert "Test-Elev" in prompt
    assert "nudge_homework" in prompt.lower() or "Läxgnäll: nej" in prompt


def test_soul_turn_blocks_without_llm(monkeypatch):
    import asyncio

    from safety import kernel_reply
    from soul import turn

    async def fake_up():
        return True

    monkeypatch.setattr("soul.ollama_up", fake_up)
    result = asyncio.run(turn("Hur gör man sex?"))
    assert result["status"] == "blocked_input"
    assert result["response"] == kernel_reply("block")
    assert result["mode"] == "soul"
