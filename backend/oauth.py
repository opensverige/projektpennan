"""Prenumerations-OAuth. Hermes-mönster, inte Claude.

ChatGPT och Grok har officiell device-inloggning för *sin* CLI
(Codex / Grok Build). Vi öppnar deras sida och kan importera den
lokala sessionen. Vi låtsas inte vara Codex eller Grok Build.

Claude: Anthropic förbjuder third-party OAuth mot Free/Pro/Max.
Ingen knapp. Nyckel eller API.
"""

from __future__ import annotations

import json
from pathlib import Path

PROVIDERS = {
    "chatgpt": {
        "allowed": True,
        "label": "ChatGPT",
        "device_url": "https://auth.openai.com/codex/device",
        "hint": "Samma inloggning som Codex. Plus eller högre. Slå på device-kod under ChatGPT → Säkerhet om den ber om det.",
        "import_files": ("~/.codex/auth.json", "~/.hermes/auth.json"),
        "token_keys": ("access_token", "refresh_token"),
    },
    "grok": {
        "allowed": True,
        "label": "Grok",
        "device_url": "https://auth.x.ai",
        "hint": "SuperGrok eller X Premium+. På en dator med terminal: grok login --device-auth.",
        "import_files": ("~/.grok/auth.json",),
        "token_keys": ("access_token", "refresh_token"),
    },
    "claude": {
        "allowed": False,
        "label": "Claude",
        "reason": "Anthropic tillåter inte att vi loggar in med ett Claude-abonnemang. Klistra en API-nyckel.",
    },
}


def catalog() -> list[dict]:
    out = []
    for key, spec in PROVIDERS.items():
        item = {"id": key, "label": spec["label"], "allowed": spec["allowed"]}
        if spec["allowed"]:
            item["device_url"] = spec["device_url"]
            item["hint"] = spec["hint"]
        else:
            item["reason"] = spec["reason"]
        out.append(item)
    return out


def get_provider(provider: str) -> dict:
    spec = PROVIDERS.get(provider)
    if not spec:
        raise KeyError(provider)
    return spec


def _has_tokens(payload: object, keys: tuple[str, ...]) -> bool:
    if not isinstance(payload, dict):
        return False
    if any(isinstance(payload.get(k), str) and payload.get(k) for k in keys):
        return True
    tokens = payload.get("tokens")
    if isinstance(tokens, dict) and any(
        isinstance(tokens.get(k), str) and tokens.get(k) for k in keys
    ):
        return True
    return False


def find_local_session(provider: str) -> dict:
    spec = get_provider(provider)
    if not spec.get("allowed"):
        return {"ok": False, "reason": spec["reason"]}
    keys = spec["token_keys"]
    for raw in spec["import_files"]:
        path = Path(raw).expanduser()
        if not path.is_file():
            continue
        try:
            data = json.loads(path.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError):
            continue
        if _has_tokens(data, keys):
            return {
                "ok": True,
                "provider": provider,
                "source": raw,
            }
    return {
        "ok": False,
        "reason": "Ingen lokal inloggning hittades än. Öppna länken, logga in, tryck igen.",
    }
