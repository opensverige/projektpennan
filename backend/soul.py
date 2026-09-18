"""Live SOUL-tur. Prompten från agents/tutor. Modellen undervisar.

Kärnan (safety.py) stoppar kris/block/hemlighet/jailbreak — in och ut.
Hjärnan är frontier eller smart OSS via providers.py. Inte Ollama-default.
"""

from __future__ import annotations

import json
import os
from pathlib import Path

from memory import maybe_note_from_child, render_for_prompt
from providers import complete, load_runtime, ping, ready
from safety import check_output_safety, classify_input, kernel_reply

ROOT = Path(__file__).resolve().parent.parent
AGENTS = ROOT / "agents" / "tutor"
VAULT = Path(os.getenv("VAULT_PATH", ROOT / "vault"))


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
        "Första drag: en sann koppling till hens värld, inte 7×7. Svenska. Inget facit.\n"
        f"\n{render_for_prompt()}\n"
    )


async def turn(
    message: str,
    history: list[dict] | None = None,
    api_key: str | None = None,
    provider: str | None = None,
) -> dict:
    text = message.strip()
    runtime = load_runtime(override_key=api_key, override_provider=provider)
    hit = classify_input(text)
    if hit["kind"] != "ok":
        return {
            "response": kernel_reply(hit["kind"]),
            "status": "blocked_input",
            "mode": "soul",
            "kind": hit["kind"],
            "model": None,
        }
    maybe_note_from_child(text)
    if not ready(runtime) or not await ping(runtime):
        return {
            "response": (
                "Ingen modell igång. Klistra ChatGPT, Grok, Claude eller Groq "
                "på startsidan, eller peka OPENAI_BASE_URL mot en lokal motor."
            ),
            "status": "error",
            "mode": "soul",
            "kind": "offline",
            "model": runtime.label() if runtime.provider != "none" else None,
        }
    convo = list(history or [])
    convo.append({"role": "user", "content": text})
    try:
        reply = await complete(build_system_prompt(), convo, runtime)
    except Exception:
        return {
            "response": "Oj, jag tappade tråden. Försök igen.",
            "status": "error",
            "mode": "soul",
            "kind": "llm_error",
            "model": runtime.label(),
        }
    if not reply:
        reply = "Jag hängde inte med. Kan du säga det igen, en bit i taget?"
    output = check_output_safety(reply, load_policies())
    if not output["safe"]:
        return {
            "response": "Jag behöver tänka lite mer på det där. Kan vi prata om något annat?",
            "status": "blocked_output",
            "mode": "soul",
            "kind": "unsafe_output",
            "model": runtime.label(),
        }
    return {
        "response": output.get("trimmed") or reply,
        "status": "ok",
        "mode": "soul",
        "kind": "llm",
        "model": runtime.label(),
    }
