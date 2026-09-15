"""
Tests för profile loader och core-funktioner.
Kräver INTE Gemini API-nyckel — testar bara datainläsning.
"""
import pytest
from pathlib import Path
import sys

# Lägg till projektrot i path
sys.path.insert(0, str(Path(__file__).parent.parent))

from skooli_buddy.profile import load_profile


def test_load_profile_returns_required_keys():
    """load_profile() ska returnera dict med child, policies och curriculum."""
    profile = load_profile()
    assert "child" in profile
    assert "policies" in profile
    assert "curriculum" in profile


def test_load_profile_child_has_data():
    """child-profilen ska ha data."""
    profile = load_profile()
    child = profile["child"]
    assert isinstance(child, dict)
    assert len(child) > 0


def test_load_profile_policies_has_data():
    """policies ska ha data."""
    profile = load_profile()
    assert isinstance(profile["policies"], dict)
    assert len(profile["policies"]) > 0


def test_load_profile_packs_are_parent_owned():
    """Kursplan är pack, inte överhet. Inget läx-nudge."""
    policies = load_profile()["policies"]
    assert policies["packs"]["curriculum_required"] is False
    assert policies["pedagogy"]["nudge_homework"] is False


def test_child_accommodations_default_empty():
    """Tom anpassning = extra-stöd-default, ingen diagnos vi satt."""
    child = load_profile()["child"].get("child", load_profile()["child"])
    acc = child.get("accommodations") or {}
    assert acc.get("parent_authored") is False
    assert acc.get("labels") == []
    assert acc.get("tell_child_the_label") is False


def test_load_profile_curriculum_has_entries():
    """curriculum ska ha minst en post."""
    profile = load_profile()
    curriculum = profile["curriculum"]
    assert isinstance(curriculum, list)
    assert len(curriculum) > 0


def test_curriculum_entries_have_required_keys():
    """Varje curriculumpost ska ha id, area, content och keywords."""
    profile = load_profile()
    required = {"id", "area", "content", "keywords", "source"}
    for entry in profile["curriculum"]:
        missing = required - set(entry.keys())
        assert not missing, f"Post {entry.get('id', '?')} saknar: {missing}"


def test_curriculum_entries_have_content():
    """Varje curriculumpost ska ha icke-tomt innehåll."""
    profile = load_profile()
    for entry in profile["curriculum"]:
        assert entry.get("content"), f"Tom content i post {entry.get('id', '?')}"
        assert entry.get("keywords"), f"Tomma keywords i post {entry.get('id', '?')}"
