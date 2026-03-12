"""
Enkel JSONL-loggning av konversationer.
GDPR-minimerad: loggar bara numeriskt chat_id, aldrig personuppgifter.
Format enligt SKOOLI_BUDDY_SAFETY_SPEC.md DEL 5.
"""
import json
import sys
from datetime import datetime, timezone
from pathlib import Path

LOGS_DIR = Path(__file__).parent.parent / "logs"


def log_turn(
    chat_id: int,
    user_msg: str,
    bot_reply: str,
    turn: int,
    blocked: bool = False,
    image_sent: bool = False,
    image_received: bool = False,
    session_messages: int = 0,
) -> None:
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
            "ts": datetime.now(tz=timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
            "chat_id": chat_id,
            "turn": turn,
            "user_text": user_msg,
            "bot_text": bot_reply,
            "blocked": blocked,
            "image_sent": image_sent,
            "image_received": image_received,
            "session_messages": session_messages,
        }

        with log_file.open("a", encoding="utf-8") as f:
            f.write(json.dumps(entry, ensure_ascii=False) + "\n")

    except Exception as e:
        print(f"Loggningsfel: {e}", file=sys.stderr)


def delete_logs_for_chat(chat_id: int) -> None:
    """
    Raderar alla loggrader kopplade till ett chat_id.
    Körs vid /revoke för att uppfylla GDPR-kravet om radering.
    """
    if not LOGS_DIR.exists():
        return
    try:
        for log_file in LOGS_DIR.glob("*.jsonl"):
            lines = log_file.read_text(encoding="utf-8").splitlines()
            kept = [
                line for line in lines
                if line.strip() and json.loads(line).get("chat_id") != chat_id
            ]
            removed = len([l for l in lines if l.strip()]) - len(kept)
            if removed > 0:
                log_file.write_text(
                    "\n".join(kept) + ("\n" if kept else ""),
                    encoding="utf-8",
                )
    except Exception as e:
        print(f"Fel vid radering av loggar för chat_id={chat_id}: {e}", file=sys.stderr)
