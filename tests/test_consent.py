"""
Tests för GDPR-samtyckesflödet.
Använder en tillfällig samtyckesfil för att inte påverka riktig data.
"""
import pytest
import json
from pathlib import Path
import sys
import tempfile
import os

# Lägg till projektrot i path
sys.path.insert(0, str(Path(__file__).parent.parent))

import skooli_buddy.consent as consent_module


@pytest.fixture(autouse=True)
def temp_consents_file(tmp_path, monkeypatch):
    """Byt ut samtyckesfilen mot en temporär fil för varje test."""
    temp_file = tmp_path / "consents.json"
    monkeypatch.setattr(consent_module, "CONSENTS_FILE", temp_file)
    yield temp_file


def test_has_consent_false_before_recording():
    """has_consent ska returnera False innan samtycke registreras."""
    assert consent_module.has_consent(12345) is False


def test_record_consent_sets_true():
    """record_consent ska göra att has_consent returnerar True."""
    consent_module.record_consent(12345)
    assert consent_module.has_consent(12345) is True


def test_revoke_consent_sets_false():
    """revoke_consent ska göra att has_consent returnerar False igen."""
    consent_module.record_consent(12345)
    assert consent_module.has_consent(12345) is True
    consent_module.revoke_consent(12345)
    assert consent_module.has_consent(12345) is False


def test_revoke_sets_pending_deletion():
    """revoke_consent ska sätta pending_deletion=True i samtyckesfilen."""
    consent_module.record_consent(12345)
    consent_module.revoke_consent(12345)

    data = json.loads(consent_module.CONSENTS_FILE.read_text(encoding="utf-8"))
    assert data["12345"]["pending_deletion"] is True


def test_multiple_chat_ids_independent():
    """Samtycken för olika chat_id ska vara oberoende av varandra."""
    consent_module.record_consent(111)
    consent_module.record_consent(222)
    consent_module.revoke_consent(111)

    assert consent_module.has_consent(111) is False
    assert consent_module.has_consent(222) is True


def test_has_consent_unknown_chat_id():
    """has_consent för okänt chat_id ska returnera False."""
    assert consent_module.has_consent(99999) is False
