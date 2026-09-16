"""Obsidian-minne i vault/memory/. Vanliga markdown-filer.

Föräldern kan öppna `vault/` som en vault i Obsidian.
Vi skriver. De äger filerna. Ingen moln-sync hos oss.
"""

from __future__ import annotations

import json
import os
import re
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
VAULT = Path(os.getenv("VAULT_PATH", ROOT / "vault"))
MEMORY = VAULT / "memory"
PROFILE = VAULT / "config" / "child-profile.json"

INTEREST_CHIPS = (
    "Minecraft",
    "Fotboll",
    "Hästar",
    "Rymden",
    "Djur",
    "Rita",
    "Musik",
    "Lego",
    "YouTube",
    "Simning",
)


def _today() -> str:
    return datetime.now(timezone.utc).date().isoformat()


def _write(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


def load_profile() -> dict:
    if not PROFILE.is_file():
        return {"schema_version": "0.2.0", "child": {}}
    try:
        return json.loads(PROFILE.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return {"schema_version": "0.2.0", "child": {}}


def interests_of(profile: dict | None = None) -> list[str]:
    child = (profile or load_profile()).get("child") or {}
    out = []
    for item in child.get("interests") or []:
        name = str(item).strip()
        if name and name not in out:
            out.append(name)
    return out


def remember_child(name: str, interests: list[str] | None = None) -> dict:
    """Uppdatera barnkort + Obsidian-sidor. Numeriskt, inget efternamn."""
    first = (name or "").strip().split()[0][:40]
    if len(first) < 2:
        raise ValueError("Namnet är för kort.")
    clean = []
    for item in interests or []:
        word = str(item).strip()[:40]
        if word and word not in clean:
            clean.append(word)
    data = load_profile()
    child = data.setdefault("child", {})
    child["display_name"] = first
    if clean:
        child["interests"] = clean
    data["updated_at"] = datetime.now(timezone.utc).isoformat()
    PROFILE.parent.mkdir(parents=True, exist_ok=True)
    PROFILE.write_text(
        json.dumps(data, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    _sync_notes(first, interests_of(data))
    return {"name": first, "interests": interests_of(data)}


def _sync_notes(name: str, interests: list[str]) -> None:
    chips = ", ".join(f"[[{i}]]" for i in interests) or "okänt än"
    _write(
        MEMORY / "barn.md",
        (
            "---\n"
            f"name: {name}\n"
            f"updated: {_today()}\n"
            "---\n\n"
            f"# {name}\n\n"
            f"Intressen: {chips}\n\n"
            "Antag att hen inte är intresserad av uppgiften. "
            "Hitta den riktiga dörren in i *hens* värld.\n"
        ),
    )
    lines = [
        "---",
        f"updated: {_today()}",
        "---",
        "",
        "# Intressen",
        "",
        "En sida per grej hen bryr sig om. Öppna vaulten i Obsidian.",
        "",
    ]
    for item in interests:
        lines.append(f"- [[{item}]]")
        _write(
            MEMORY / f"{_slug(item)}.md",
            (
                "---\n"
                f"interest: {item}\n"
                f"updated: {_today()}\n"
                "---\n\n"
                f"# {item}\n\n"
                "Vad är sant i den här världen som *är* samma idé som "
                "läxan — inte en söt belöning ovanpå den?\n"
            ),
        )
    _write(MEMORY / "intressen.md", "\n".join(lines) + "\n")
    if not (MEMORY / "gnistor.md").is_file():
        _write(
            MEMORY / "gnistor.md",
            (
                "---\n"
                f"updated: {_today()}\n"
                "---\n\n"
                "# Gnistor\n\n"
                "Vad tände. Vad släckte. En rad i taget.\n"
            ),
        )
    if not (MEMORY / "README.md").is_file():
        _write(
            MEMORY / "README.md",
            (
                "# Minne\n\n"
                "Öppna mappen `vault/` i [Obsidian](https://obsidian.md). "
                "Det är vanliga markdown-filer. Vi skriver. Ni äger.\n"
            ),
        )


def _slug(name: str) -> str:
    text = re.sub(r"[^\w\s-]", "", name, flags=re.UNICODE).strip().lower()
    text = re.sub(r"[\s_]+", "-", text)
    return text or "intresse"


def note_spark(kind: str, text: str) -> None:
    """kind: tande | slack | intresse"""
    path = MEMORY / "gnistor.md"
    if not path.is_file():
        _sync_notes(
            (load_profile().get("child") or {}).get("display_name") or "Elev",
            interests_of(),
        )
    line = f"- {_today()} · {kind}: {text.strip()[:180]}\n"
    with path.open("a", encoding="utf-8") as handle:
        handle.write(line)


def render_for_prompt() -> str:
    interests = interests_of()
    sparks = ""
    path = MEMORY / "gnistor.md"
    if path.is_file():
        body = path.read_text(encoding="utf-8")
        rows = [ln for ln in body.splitlines() if ln.startswith("- ")]
        sparks = "\n".join(rows[-8:])
    names = ", ".join(interests) or "okänt — fråga en sak om deras värld först"
    return (
        "## Minne (Obsidian-vault)\n"
        f"- Intressen: {names}\n"
        "- Anta ointresse för uppgiften. Hitta en *sann* koppling.\n"
        "- Inte: Minecraft + 4+3. Inte: vill du göra matteläxan.\n"
        + (f"\nSenaste gnistor:\n{sparks}\n" if sparks else "")
    )


def maybe_note_from_child(message: str) -> None:
    text = (message or "").lower()
    for item in interests_of():
        if item.lower() in text:
            note_spark("intresse", f"nämnde {item}")
            return
    if any(w in text for w in ("tråkigt", "hatar", "orkar inte", "skit")):
        note_spark("slack", message[:120])
