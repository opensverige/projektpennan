"""Utility helpers for guardian reports stored under vault/parent-reports."""

from __future__ import annotations

import json
import os
from pathlib import Path
from typing import Dict, List, Optional

VAULT_PATH = Path(os.getenv("VAULT_PATH", "/app/vault"))
REPORTS_DIR = VAULT_PATH / "parent-reports"


def _report_path(report_id: str) -> Path:
    return REPORTS_DIR / f"{report_id}.json"


def list_reports() -> List[Dict]:
    if not REPORTS_DIR.exists():
        return []

    reports: List[Dict] = []
    for path in sorted(REPORTS_DIR.glob("*.json")):
        data = _load_json(path)
        if not data:
            continue
        reports.append(
            {
                "id": data.get("id") or path.stem,
                "title": data.get("title", "Rapport"),
                "period": data.get("period", ""),
                "summary": data.get("summary", ""),
                "updated_at": path.stat().st_mtime,
            }
        )
    reports.sort(key=lambda item: item["updated_at"], reverse=True)
    return reports


def get_report(report_id: str) -> Optional[Dict]:
    path = _report_path(report_id)
    if path.exists():
        data = _load_json(path)
        if data:
            data.setdefault("id", report_id)
            return data

    # fallback: search by embedded id
    for candidate in REPORTS_DIR.glob("*.json"):
        data = _load_json(candidate)
        if data and str(data.get("id")) == report_id:
            return data
    return None


def _load_json(path: Path) -> Optional[Dict]:
    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
    except (FileNotFoundError, json.JSONDecodeError):
        return None
    if not isinstance(payload, dict):
        return None
    return payload
