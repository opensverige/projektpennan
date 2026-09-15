"""Pack-manifest och policies. Ingen nätverk, ingen API-nyckel."""
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
PACKS = ROOT / "vault" / "packs"
SCHEMA = PACKS / "_schema" / "manifest.schema.json"
KINDS = {
    "curriculum",
    "worldview",
    "pedagogy",
    "accommodations",
    "custom-agent",
    "school-context",
}
REQUIRED = {
    "id",
    "name",
    "kind",
    "enabled",
    "authored_by",
    "version",
    "can_disable",
    "cannot_override_safety",
}


def _manifests() -> list[Path]:
    return sorted(p for p in PACKS.glob("*/manifest.json") if p.is_file())


def test_pack_schema_file_exists():
    schema = json.loads(SCHEMA.read_text(encoding="utf-8"))
    assert schema["title"]
    assert schema["properties"]["cannot_override_safety"]["const"] is True


def test_example_packs_exist():
    kinds_found = set()
    paths = _manifests()
    assert paths, "inga pack-manifest i vault/packs/"
    for path in paths:
        data = json.loads(path.read_text(encoding="utf-8"))
        missing = REQUIRED - set(data)
        assert not missing, f"{path.parent.name} saknar {missing}"
        assert data["cannot_override_safety"] is True
        assert data["kind"] in KINDS
        kinds_found.add(data["kind"])
    assert kinds_found == KINDS


def test_lgr22_pack_is_optional():
    data = json.loads((PACKS / "lgr22" / "manifest.json").read_text(encoding="utf-8"))
    assert data["can_disable"] is True
    assert data["kind"] == "curriculum"


def test_worldview_pack_starts_off():
    data = json.loads((PACKS / "worldview" / "manifest.json").read_text(encoding="utf-8"))
    assert data["enabled"] is False
    overlay = (PACKS / "worldview" / "OVERLAY.md").read_text(encoding="utf-8")
    assert "Neutral är default" in overlay


def test_school_context_pack_is_parent_owned_and_minimized():
    data = json.loads((PACKS / "school-context" / "manifest.json").read_text(encoding="utf-8"))
    assert data["enabled"] is False
    assert data["kind"] == "school-context"
    ctx = json.loads((PACKS / "school-context" / "context.json").read_text(encoding="utf-8"))
    assert ctx["nudge_homework"] is False
    assert ctx["write_back_to_school"] is False
    assert "grades" in ctx["dropped"]
    assert "credentials" in ctx["dropped"]


def test_policies_mark_curriculum_not_required():
    for rel in ("config/policies.json", "vault/config/policies.json"):
        policies = json.loads((ROOT / rel).read_text(encoding="utf-8"))
        packs = policies["packs"]
        assert packs["curriculum_required"] is False
        assert packs["allow_parent_uploads"] is True
        assert packs.get("school_context") in (None, "school-context-family")
        assert policies["parent_controls"]["school_integration"] is False
        assert policies["parent_controls"]["school_context_ingest"] in ("off", "parent_owned")
        assert policies["pedagogy"]["nudge_homework"] is False
        modes = set(policies["pedagogy"]["allowed_modes"])
        assert {"sokratisk", "worked", "cpa", "story", "play", "retrieve"} <= modes
