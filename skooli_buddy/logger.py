"""
Enkel JSONL-loggning av konversationer.
GDPR-minimerad: loggar bara numeriskt chat_id, aldrig personuppgifter.
"""
import json
import sys
from datetime import datetime, timezone
from pathlib import Path

LOGS_DIR = Path(__file__).parent.parent / "logs"


def log_turn(chat_id: int, user_msg: str, bot_reply: str) -> None:
    """
    Loggar en konversationstur till en dagsfil i logs/.
    Format: logs/2026-03-12.jsonl — en JSON-rad per tur.
    Loggar ALDRIG namn, användarnamn eller andra personuppgifter.
    """
    try:
        LOGS_DIR.mkdir(exist_ok=True)
        today = datetime.now(tz=timezone.utc).strftime("%Y-%m-%d")
        log_file = LOGS_DIR / f"{today}.jsonl"

        entry = {
            "ts": datetime.now(tz=timezone.utc).isoformat(),
            "chat_id": chat_id,
            "user": user_msg,
            "bot": bot_reply,
        }

        with log_file.open("a", encoding="utf-8") as f:
            f.write(json.dumps(entry, ensure_ascii=False) + "\n")

    except Exception as e:
        print(f"Loggningsfel: {e}", file=sys.stderr)
