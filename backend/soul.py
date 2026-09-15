"""Live SOUL-tur. Prompten från agents/tutor. Modellen undervisar.

Kärnan (safety.py) stoppar kris/block/hemlighet/jailbreak.
Läxa och vanligt snack går till Ollama — inte till stubbarna.
"""

from __future__ import annotations

import json
import os
from pathlib import Path

import httpx

from safety import classify_input, kernel_reply

ROOT = Path(__file__).resolve().parent.parent
AGENTS = ROOT / "agents" / "tutor"
VAULT = Path(os.getenv("VAULT_PATH", ROOT / "vault"))
OLLAMA_URL = os.getenv("OLLAMA_URL", "http://127.0.0.1:11434").rstrip("/")
MODEL_NAME = os.getenv("MODEL_NAME", "llama3.2:3b")


def load_json(path: Path) -> dict:
    if not path.is_file():
        raise FileNotFoundError(f"Saknas: {path}")
    return json.loads(path.read_text(encoding="utf-8"))


def load_profile() -> dict:
    return load_json(VAULT / "config" / "child-profile.json")


def load_policies() -> dict:
    return load_json(VAULT / "config" / "policies.json")


def build_system_prompt(profile: dict | None = None, policies: dict | None = None) -> str:
    profile = profile or load_profile()
    policies = policies or load_policies()
    soul = (AGENTS / "SOUL.md").read_text(encoding="utf-8")
    skill = (AGENTS / "SKILL.md").read_text(encoding="utf-8")
    rules = (AGENTS / "RULES.md").read_text(encoding="utf-8")
    child = profile.get("child", {})
    pedagogy = policies.get("pedagogy", {})
    packs = policies.get("packs", {})
    return (
        f"{soul}\n\n---\n\n{skill}\n\n---\n\n{rules}\n\n---\n\n"
        "## Aktuell elev\n"
        f"- Namn: {child.get('display_name', 'Elev')}\n"
        f"- Årskurs: {child.get('grade', '?')}\n"
        f"- Ålder: {child.get('age', '?')}\n"
        f"- Språk: {child.get('language', 'sv')}\n"
        f"- Ämnen: {', '.join(child.get('subjects') or [])}\n"
        f"- Intressen: {', '.join(child.get('interests') or [])}\n"
        f"- Stöd: {', '.join(child.get('support_preferences') or [])}\n"
        f"- Kursplan-pack: {packs.get('curriculum') or 'av'}\n"
        f"- Världsbild-pack: {packs.get('worldview') or 'ingen'}\n"
        f"- Metoder: {', '.join(pedagogy.get('allowed_modes') or [])}\n"
        f"- Läxgnäll: {'ja' if pedagogy.get('nudge_homework') else 'nej'}\n"
        "\n## Just den här turen\n"
        "Svara på det barnet skrev. BRIS 116 111 bara vid kris, aldrig i matte.\n"
        "Max två korta meningar och en fråga. Svenska. Inget facit först.\n"
    )


async def call_ollama(system_prompt: str, history: list[dict]) -> str:
    messages = [{"role": "system", "content": system_prompt}, *history]
    async with httpx.AsyncClient(timeout=120.0) as client:
        response = await client.post(
            f"{OLLAMA_URL}/api/chat",
            json={
                "model": MODEL_NAME,
                "messages": messages,
                "stream": False,
                "options": {"temperature": 0.7, "num_predict": 256},
            },
        )
        response.raise_for_status()
        data = response.json()
    return (data.get("message") or {}).get("content", "").strip()


async def ollama_up() -> bool:
    try:
        async with httpx.AsyncClient(timeout=2.0) as client:
            res = await client.get(f"{OLLAMA_URL}/api/tags")
        return res.status_code == 200
    except httpx.HTTPError:
        return False


async def turn(message: str, history: list[dict] | None = None) -> dict:
    text = message.strip()
    hit = classify_input(text)
    if hit["kind"] != "ok":
        return {
            "response": kernel_reply(hit["kind"]),
            "status": "blocked_input",
            "mode": "soul",
            "kind": hit["kind"],
            "model": None,
        }
    if not await ollama_up():
        return {
            "response": "SOUL sover. Starta Ollama och ./scripts/soul.sh.",
            "status": "error",
            "mode": "soul",
            "kind": "offline",
            "model": MODEL_NAME,
        }
    convo = list(history or [])
    convo.append({"role": "user", "content": text})
    try:
        reply = await call_ollama(build_system_prompt(), convo)
    except Exception as exc:
        return {
            "response": "Oj, jag tappade tråden. Försök igen.",
            "status": "error",
            "mode": "soul",
            "kind": "llm_error",
            "model": MODEL_NAME,
            "detail": str(exc),
        }
    if not reply:
        reply = "Jag hängde inte med. Kan du säga det igen, en bit i taget?"
    return {
        "response": reply,
        "status": "ok",
        "mode": "soul",
        "kind": "llm",
        "model": MODEL_NAME,
    }
