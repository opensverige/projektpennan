"""
Deterministisk säkerhetsfiltrering. Ingen LLM. Bara kod.
Principen: LLM:en undervisar. Koden validerar.
"""

from __future__ import annotations

import json
import re
from pathlib import Path

VAULT_PATH = Path("/app/vault")


def load_policies() -> dict:
    policies_path = VAULT_PATH / "config" / "policies.json"
    if not policies_path.exists():
        raise FileNotFoundError(f"CRITICAL: {policies_path} saknas. Starta inte utan config.")
    return json.loads(policies_path.read_text(encoding="utf-8"))


KERNEL_REPLIES = {
    "crisis": (
        "Jag hör dig, och det du känner är viktigt. "
        "Prata med en vuxen du litar på — en förälder, en lärare, "
        "eller ring BRIS på 116 111. De lyssnar alltid, och det kostar inget att ringa."
    ),
    "secret": (
        "Jag håller inga hemligheter från din förälder. "
        "Vill du berätta vad som kärvar i läxan i stället?"
    ),
    "block": (
        "Den frågan pratar du med en vuxen hemma om. Inte med mig. "
        "Vill du ha hjälp med något annat?"
    ),
    "jailbreak": (
        "Jag är Gnista, en studiekompis din förälder slagit på. "
        "Reglerna sitter i koden. De går inte att byta. Vad kärvar i läxan?"
    ),
}

# Kris först. Sedan hemlighet, jailbreak, block. Svenska + engelska.
_CRISIS = [
    r"\b(suicide|selfharm|self-harm)\b",
    r"\b(ta livet|ta mitt liv|inte leva mer|inte leva längre)\b",
    r"\b(vill inte leva|önskar att jag var död)\b",
    r"\b(självskad|skada mig|skära mig)\b",
]
_SECRET = [
    r"lova att inte berätta",
    r"säg inte till (mamma|pappa|föräldern|mamma|pappa)",
    r"hemlighet från (mamma|pappa|föräldern|förälder)",
    r"don't tell (mom|dad|my parents)",
    r"keep this (a )?secret",
]
_JAILBREAK = [
    r"glöm (alla )?reglerna",
    r"ignorera (dina )?(instruktion|regler)",
    r"du är min hemliga (kompis|vän)",
    r"\bjailbreak\b",
    r"pretend you are",
    r"ignore (your )?(instructions|rules)",
]
_BLOCK = [
    r"\b(porn|porr|knull|naken|nude|naked)\b",
    r"hur gör man sex",
    r"\bha sex\b",
    r"\b(cocaine|heroin|meth|kokain)\b",
    r"\b(bomb|vapen|vapnet)\b",
    r"hur bygger man en bomb",
    r"\b(murder|suicide)\b",
    r"knife\s+attack",
]

COMPILED = {
    "crisis": [re.compile(p, re.IGNORECASE) for p in _CRISIS],
    "secret": [re.compile(p, re.IGNORECASE) for p in _SECRET],
    "jailbreak": [re.compile(p, re.IGNORECASE) for p in _JAILBREAK],
    "block": [re.compile(p, re.IGNORECASE) for p in _BLOCK],
}

KIND_ORDER = ("crisis", "secret", "jailbreak", "block")


def classify_input(user_message: str) -> dict:
    text = user_message or ""
    for kind in KIND_ORDER:
        for pattern in COMPILED[kind]:
            if pattern.search(text):
                return {"kind": kind, "reason": pattern.pattern, "safe": False}
    return {"kind": "ok", "reason": None, "safe": True}


def check_input_safety(user_message: str) -> dict:
    """
    Kontrollera barnets meddelande INNAN det skickas till LLM.
    Returnerar: {"safe": bool, "reason": str|None, "kind": str}
    """
    return classify_input(user_message)


def kernel_reply(kind: str) -> str:
    return KERNEL_REPLIES.get(kind, KERNEL_REPLIES["block"])


def check_output_safety(llm_response: str, policies: dict) -> dict:
    """
    Kontrollera LLM-svaret INNAN det skickas till barnet.
    Returnerar: {"safe": bool, "reason": str|None, "trimmed": str|None}
    """
    for kind in ("block", "crisis"):
        for pattern in COMPILED[kind]:
            if pattern.search(llm_response):
                return {
                    "safe": False,
                    "reason": f"LLM output contained blocked pattern: {pattern.pattern}",
                    "trimmed": None,
                }

    max_chars = policies.get("safety", {}).get("max_response_length_chars", 500)
    trimmed = None
    if len(llm_response) > max_chars:
        trimmed = llm_response[:max_chars] + "..."

    return {"safe": True, "reason": None, "trimmed": trimmed}
