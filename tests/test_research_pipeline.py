"""Tester för research-pipelinen. Inget nätverk, ingen API-nyckel."""
from __future__ import annotations

import json
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "scripts"))

import research_pipeline as rp  # noqa: E402


def test_findings_validate_clean():
    assert rp.cmd_validate() == 0


def test_findings_have_unique_ids():
    findings = rp.load_findings()
    ids = [f["id"] for f in findings]
    assert ids, "inga fynd"
    assert len(ids) == len(set(ids))


def test_sources_have_unique_ids():
    payload = rp.load_sources()
    ids = [s["id"] for s in payload["sources"]]
    assert ids
    assert len(ids) == len(set(ids))


def test_accepted_findings_point_at_real_backlog():
    backlog = rp.BACKLOG_FILE.read_text(encoding="utf-8")
    known = rp.extract_backlog_ids(backlog)
    for finding in rp.load_findings():
        if finding.get("status") != "accepted":
            continue
        for ref in finding.get("backlog_refs", []):
            assert ref in known, f"{finding['id']} pekar på okänd {ref}"


def test_validate_finding_rejects_short_claim():
    finding = {
        "id": "kort",
        "date": "2026-09-15",
        "theme": "pedagogy",
        "status": "draft",
        "claim": "för kort",
        "evidence": [
            {
                "title": "En källa",
                "url": "https://example.org/x",
                "year": 2026,
                "notes": "Tillräckligt lång notering.",
            }
        ],
        "implication": "Det här är en tillräckligt lång implikation.",
        "backlog_refs": ["P-01"],
        "confidence": "low",
        "_path": "research/findings/kort.json",
    }
    errors = rp.validate_finding(finding, set(), {"P-01"})
    assert any("claim" in e for e in errors)


def test_validate_finding_rejects_unknown_backlog_ref():
    finding = {
        "id": "okand-ref",
        "date": "2026-09-15",
        "theme": "safety",
        "status": "accepted",
        "claim": "Ett påstående som är tillräckligt långt för schemat.",
        "evidence": [
            {
                "title": "En källa",
                "url": "https://example.org/x",
                "year": 2026,
                "notes": "Tillräckligt lång notering.",
            }
        ],
        "implication": "Det här är en tillräckligt lång implikation.",
        "backlog_refs": ["P-99"],
        "confidence": "high",
        "_path": "research/findings/okand-ref.json",
    }
    errors = rp.validate_finding(finding, set(), {"P-01"})
    assert any("P-99" in e for e in errors)


def test_new_writes_template(tmp_path, monkeypatch):
    monkeypatch.setattr(rp, "FINDINGS_DIR", tmp_path)
    assert rp.cmd_new("testfynd-nytt", "Ett prövbart påstående om lärandeformer", "pedagogy") == 0
    payload = json.loads((tmp_path / "testfynd-nytt.json").read_text(encoding="utf-8"))
    assert payload["id"] == "testfynd-nytt"
    assert payload["theme"] == "pedagogy"
    assert payload["status"] == "draft"


def test_new_rejects_existing(tmp_path, monkeypatch):
    monkeypatch.setattr(rp, "FINDINGS_DIR", tmp_path)
    (tmp_path / "finns-redan.json").write_text("{}", encoding="utf-8")
    assert rp.cmd_new("finns-redan", "Ett prövbart påstående om lärandeformer", "product") == 1


def test_schema_file_exists():
    schema = json.loads(rp.SCHEMA_FILE.read_text(encoding="utf-8"))
    assert schema["required"]
    assert "claim" in schema["required"]
