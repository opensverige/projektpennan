"""
GDPR-samtyckesflöde för Skooli Buddy.
Barn 10-12 år faller under digital samtyckesålder (13 år i Sverige).
Förälders samtycke krävs INNAN barnet får använda boten — detta är lag.
"""
import json
import sys
from datetime import datetime, timezone
from pathlib import Path

CONSENTS_FILE = Path(__file__).parent.parent / "config" / "consents.json"


def _load_consents() -> dict:
    """Laddar samtyckesfilen. Returnerar tomt dict om filen saknas."""
    if not CONSENTS_FILE.exists():
        return {}
    try:
        return json.loads(CONSENTS_FILE.read_text(encoding="utf-8"))
    except Exception as e:
        print(f"Fel vid inläsning av samtycken: {e}", file=sys.stderr)
        return {}


def _save_consents(consents: dict) -> None:
    """Sparar samtyckesfilen."""
    try:
        CONSENTS_FILE.parent.mkdir(exist_ok=True)
        CONSENTS_FILE.write_text(
            json.dumps(consents, ensure_ascii=False, indent=2),
            encoding="utf-8",
        )
    except Exception as e:
        print(f"Fel vid sparning av samtycken: {e}", file=sys.stderr)


def has_consent(chat_id: int) -> bool:
    """Returnerar True om föräldern har gett samtycke för detta chat_id."""
    consents = _load_consents()
    entry = consents.get(str(chat_id), {})
    return bool(entry.get("consented", False))


def record_consent(chat_id: int) -> None:
    """Registrerar förälders samtycke för ett chat_id."""
    consents = _load_consents()
    consents[str(chat_id)] = {
        "consented": True,
        "timestamp": datetime.now(tz=timezone.utc).isoformat(),
    }
    _save_consents(consents)


def revoke_consent(chat_id: int) -> None:
    """
    Återkallar samtycke och markerar för datarensning.
    Sätter consented=False och flaggar pending_deletion=True.
    """
    consents = _load_consents()
    consents[str(chat_id)] = {
        "consented": False,
        "timestamp": datetime.now(tz=timezone.utc).isoformat(),
        "pending_deletion": True,
    }
    _save_consents(consents)
