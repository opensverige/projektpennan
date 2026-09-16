"""Telegram-länk utan officiell bot och utan att vi sitter på token.

Föräldern skapar boten hos @BotFather. Vi verifierar token med getMe
här hemma. En start-länk släpper in just deras chatt. Tom allowlist
+ ingen start-token = vägra starta.
"""

from __future__ import annotations

import json
import os
import secrets
import urllib.error
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
VAULT = Path(os.getenv("VAULT_PATH", ROOT / "vault"))
STATE_FILE = VAULT / "config" / "telegram.json"
TOKEN_FILE = VAULT / "config" / "telegram-bot-token.txt"


def _state_path() -> Path:
    return Path(os.getenv("GNISTA_TELEGRAM_STATE", STATE_FILE))


def _token_path() -> Path:
    return Path(os.getenv("GNISTA_TELEGRAM_TOKEN_FILE", TOKEN_FILE))


def load_state() -> dict:
    path = _state_path()
    if not path.is_file():
        return {
            "bot_username": None,
            "start_token": None,
            "allowed_chat_ids": [],
        }
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return {
            "bot_username": None,
            "start_token": None,
            "allowed_chat_ids": [],
        }
    ids = data.get("allowed_chat_ids") or []
    return {
        "bot_username": data.get("bot_username"),
        "start_token": data.get("start_token"),
        "allowed_chat_ids": [int(x) for x in ids],
    }


def save_state(state: dict) -> None:
    path = _state_path()
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps(
            {
                "bot_username": state.get("bot_username"),
                "start_token": state.get("start_token"),
                "allowed_chat_ids": [int(x) for x in state.get("allowed_chat_ids") or []],
            },
            ensure_ascii=False,
            indent=2,
        )
        + "\n",
        encoding="utf-8",
    )


def env_allowed_ids() -> list[int]:
    raw = os.getenv("TELEGRAM_ALLOWED_CHAT_IDS", "").strip()
    if not raw:
        return []
    out = []
    for part in raw.split(","):
        part = part.strip()
        if part.lstrip("-").isdigit():
            out.append(int(part))
    return out


def allowed_chat_ids() -> set[int]:
    ids = set(load_state()["allowed_chat_ids"])
    ids.update(env_allowed_ids())
    return ids


def bot_token() -> str | None:
    env = os.getenv("TELEGRAM_BOT_TOKEN", "").strip()
    if env:
        return env
    path = _token_path()
    if path.is_file():
        text = path.read_text(encoding="utf-8").strip()
        return text or None
    return None


def can_start() -> tuple[bool, str]:
    if not bot_token():
        return False, "Ingen Telegram-token. Klistra den i starten."
    if allowed_chat_ids() or load_state().get("start_token"):
        return True, "ok"
    return False, "Ingen allowlist och ingen start-länk. Klistra token i starten."


def is_allowed(chat_id: int) -> bool:
    return int(chat_id) in allowed_chat_ids()


def invite_url(username: str | None, start_token: str | None) -> str | None:
    if not username or not start_token:
        return None
    handle = username[1:] if username.startswith("@") else username
    return f"https://t.me/{handle}?start={start_token}"


def get_me(token: str) -> dict:
    req = urllib.request.Request(
        f"https://api.telegram.org/bot{token}/getMe",
        method="GET",
    )
    try:
        with urllib.request.urlopen(req, timeout=8) as res:
            payload = json.loads(res.read().decode("utf-8"))
    except (urllib.error.URLError, TimeoutError, json.JSONDecodeError, OSError) as exc:
        raise ValueError("Telegram svarade inte. Kolla token.") from exc
    if not payload.get("ok") or not payload.get("result", {}).get("username"):
        raise ValueError("Det där var inte en giltig bot-token.")
    return payload["result"]


def bind_token(token: str, username: str) -> dict:
    token = token.strip()
    if ":" not in token or len(token) < 20:
        raise ValueError("Det där ser inte ut som en bot-token.")
    start = secrets.token_urlsafe(16).replace("_", "").replace("-", "")[:24]
    state = load_state()
    state["bot_username"] = username
    state["start_token"] = start
    save_state(state)
    path = _token_path()
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(token + "\n", encoding="utf-8")
    return {
        "ok": True,
        "username": username,
        "invite": invite_url(username, start),
        "start_token": start,
    }


def verify_and_bind(token: str, fetcher=get_me) -> dict:
    me = fetcher(token.strip())
    return bind_token(token, me["username"])


def claim_start(chat_id: int, payload: str | None) -> bool:
    if is_allowed(chat_id):
        return True
    state = load_state()
    token = state.get("start_token")
    if not token or not payload or payload != token:
        return False
    ids = state.get("allowed_chat_ids") or []
    if int(chat_id) not in ids:
        ids.append(int(chat_id))
    state["allowed_chat_ids"] = ids
    save_state(state)
    return True


def public_status() -> dict:
    state = load_state()
    return {
        "username": state.get("bot_username"),
        "invite": invite_url(state.get("bot_username"), state.get("start_token")),
        "linked": bool(state.get("allowed_chat_ids")),
        "ready": bool(state.get("start_token") or state.get("allowed_chat_ids")),
    }
