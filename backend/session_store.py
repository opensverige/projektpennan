"""SQLite-baserad session store för chatthistorik.

Historiken lagras som JSON-array i `vault/session-store.db`. Varje save
ersätter hela historiken för sessionen men vi håller oss till max 40
poster (20 användar/assistent-par) precis som RAM-varianten.
"""

from __future__ import annotations

import json
import sqlite3
from datetime import datetime, timezone
from pathlib import Path
from typing import List, Dict


class SessionStore:
    def __init__(self, db_path: Path):
        self.db_path = Path(db_path)
        self.db_path.parent.mkdir(parents=True, exist_ok=True)
        self._init_db()

    def _init_db(self) -> None:
        with sqlite3.connect(self.db_path) as conn:
            conn.execute("PRAGMA journal_mode=WAL;")
            conn.execute("PRAGMA synchronous=NORMAL;")
            conn.execute(
                """
                CREATE TABLE IF NOT EXISTS sessions (
                    session_id TEXT PRIMARY KEY,
                    history TEXT NOT NULL,
                    updated_at TEXT NOT NULL
                )
                """
            )

    def get_history(self, session_id: str) -> List[Dict]:
        with sqlite3.connect(self.db_path) as conn:
            row = conn.execute(
                "SELECT history FROM sessions WHERE session_id = ?",
                (session_id,),
            ).fetchone()

        if not row:
            return []

        try:
            history = json.loads(row[0])
            if isinstance(history, list):
                return history
        except json.JSONDecodeError:
            pass
        return []

    def save_history(self, session_id: str, history: List[Dict]) -> None:
        serialized = json.dumps(history, ensure_ascii=False)
        timestamp = datetime.now(timezone.utc).isoformat()
        with sqlite3.connect(self.db_path) as conn:
            conn.execute(
                """
                INSERT INTO sessions(session_id, history, updated_at)
                VALUES (?, ?, ?)
                ON CONFLICT(session_id)
                DO UPDATE SET history=excluded.history, updated_at=excluded.updated_at
                """,
                (session_id, serialized, timestamp),
            )
            conn.commit()

    def clear_session(self, session_id: str) -> None:
        with sqlite3.connect(self.db_path) as conn:
            conn.execute("DELETE FROM sessions WHERE session_id = ?", (session_id,))
            conn.commit()
