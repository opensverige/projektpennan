"""En kärna. Telegram anropar samma pipeline som webben.

Ingen Gemini-egen prompt. Safety sitter i backend/safety.py.
"""

from __future__ import annotations

import asyncio
import base64
import os
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
BACKEND = ROOT / "backend"
if str(BACKEND) not in sys.path:
    sys.path.insert(0, str(BACKEND))

from pipeline import run_pipeline
from session_store import SessionStore


def _store() -> SessionStore:
    vault = Path(os.getenv("VAULT_PATH", ROOT / "vault"))
    return SessionStore(vault / "session-store.db")


def _sid(chat_id: int) -> str:
    return f"tg-{chat_id}"


async def get_response_async(
    chat_id: int,
    user_message: str,
    image: bytes | None = None,
) -> str:
    store = _store()
    session_id = _sid(chat_id)
    history = store.get_history(session_id)
    text = (user_message or "").strip() or ("foto av läxan" if image else "")
    photo = None
    if image:
        photo = "data:image/jpeg;base64," + base64.b64encode(image).decode("ascii")
    result = await run_pipeline(session_id, text, history, image=photo)
    if result.get("status") == "ok":
        history.append({"role": "user", "content": text})
        history.append({"role": "assistant", "content": result["response"]})
        if len(history) > 40:
            history[:] = history[-40:]
        store.save_history(session_id, history)
    return result.get("response") or "Oj, jag tappade tråden. Kan du försöka igen?"


def get_response(chat_id: int, user_message: str, image: bytes | None = None) -> str:
    return asyncio.run(get_response_async(chat_id, user_message, image))


def reset_chat(chat_id: int) -> None:
    _store().save_history(_sid(chat_id), [])
