"""Telegram är en yta. Pipelinen är kärnan."""

import asyncio
import base64
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).parent.parent))

from skooli_buddy import core


def test_core_is_not_a_second_prompt():
    source = Path(core.__file__).read_text(encoding="utf-8")
    assert "run_pipeline" in source
    assert "generativeai" not in source
    assert "You are" not in source


def test_telegram_calls_pipeline_with_photo(monkeypatch, tmp_path):
    captured = {}

    class FakeStore:
        def get_history(self, session_id):
            captured["session_id"] = session_id
            return []

        def save_history(self, session_id, history):
            captured["history"] = history

    async def fake_pipeline(session_id, text, history, image=None, **kwargs):
        captured["text"] = text
        captured["image"] = image
        return {"status": "ok", "response": "Minecraft. Vad är dimma?"}

    monkeypatch.setattr(core, "_store", lambda: FakeStore())
    monkeypatch.setattr(core, "run_pipeline", fake_pipeline)
    blob = b"\xff\xd8\xff" + b"abcd" * 20
    reply = asyncio.run(core.get_response_async(42, "", image=blob))
    assert reply == "Minecraft. Vad är dimma?"
    assert captured["session_id"] == "tg-42"
    assert captured["text"] == "foto av läxan"
    assert captured["image"].startswith("data:image/jpeg;base64,")
    decoded = base64.b64decode(captured["image"].split(",", 1)[1])
    assert decoded == blob
    assert captured["history"][-1]["content"] == reply
