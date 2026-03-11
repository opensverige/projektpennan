"""
Deterministisk säkerhetsfiltrering. Ingen LLM. Bara kod.
Principen: LLM:en undervisar. Koden validerar.
"""

import re
import json
from pathlib import Path

VAULT_PATH = Path("/app/vault")


def load_policies() -> dict:
    policies_path = VAULT_PATH / "config" / "policies.json"
    if not policies_path.exists():
        raise FileNotFoundError(f"CRITICAL: {policies_path} saknas. Starta inte utan config.")
    return json.loads(policies_path.read_text(encoding="utf-8"))


# Utöka denna lista. Den är medvetet minimal för scaffolding.
BLOCKED_PATTERNS = [
    r"\b(kill|murder|suicide|selfharm)\b",
    r"\b(porn|sex|naked|nude)\b",
    r"\b(drug|cocaine|heroin|meth)\b",
    r"\b(bomb|weapon|gun|knife\s+attack)\b",
]

COMPILED_PATTERNS = [re.compile(p, re.IGNORECASE) for p in BLOCKED_PATTERNS]


def check_input_safety(user_message: str) -> dict:
    """
    Kontrollera barnets meddelande INNAN det skickas till LLM.
    Returnerar: {"safe": bool, "reason": str|None}
    """
    for pattern in COMPILED_PATTERNS:
        if pattern.search(user_message):
            return {
                "safe": False,
                "reason": f"Blocked pattern detected: {pattern.pattern}"
            }

    return {"safe": True, "reason": None}


def check_output_safety(llm_response: str, policies: dict) -> dict:
    """
    Kontrollera LLM-svaret INNAN det skickas till barnet.
    Returnerar: {"safe": bool, "reason": str|None, "trimmed": str|None}
    """
    # 1. Kolla blockmönster i output också
    for pattern in COMPILED_PATTERNS:
        if pattern.search(llm_response):
            return {
                "safe": False,
                "reason": f"LLM output contained blocked pattern: {pattern.pattern}",
                "trimmed": None
            }

    # 2. Kolla max längd
    max_chars = policies.get("safety", {}).get("max_response_length_chars", 500)
    trimmed = None
    if len(llm_response) > max_chars:
        trimmed = llm_response[:max_chars] + "..."

    return {"safe": True, "reason": None, "trimmed": trimmed}
