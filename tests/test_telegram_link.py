import json

from skooli_buddy.telegram_link import (
    bind_token,
    can_start,
    claim_start,
    is_allowed,
    load_state,
    public_status,
    verify_and_bind,
)


def test_empty_state_cannot_start(monkeypatch, tmp_path):
    monkeypatch.setenv("UTTER_TELEGRAM_STATE", str(tmp_path / "telegram.json"))
    monkeypatch.setenv("UTTER_TELEGRAM_TOKEN_FILE", str(tmp_path / "token.txt"))
    monkeypatch.delenv("TELEGRAM_BOT_TOKEN", raising=False)
    monkeypatch.delenv("TELEGRAM_ALLOWED_CHAT_IDS", raising=False)
    ok, reason = can_start()
    assert ok is False
    assert "token" in reason.lower()


def test_hardcoded_dev_id_is_not_implicit(monkeypatch, tmp_path):
    monkeypatch.setenv("UTTER_TELEGRAM_STATE", str(tmp_path / "telegram.json"))
    monkeypatch.setenv("UTTER_TELEGRAM_TOKEN_FILE", str(tmp_path / "token.txt"))
    monkeypatch.setenv("TELEGRAM_BOT_TOKEN", "1:AA-fake")
    monkeypatch.delenv("TELEGRAM_ALLOWED_CHAT_IDS", raising=False)
    assert is_allowed(544123218) is False
    ok, _ = can_start()
    assert ok is False


def test_verify_binds_invite_without_leaking_token(monkeypatch, tmp_path):
    monkeypatch.setenv("UTTER_TELEGRAM_STATE", str(tmp_path / "telegram.json"))
    monkeypatch.setenv("UTTER_TELEGRAM_TOKEN_FILE", str(tmp_path / "token.txt"))

    def fake_me(_token):
        return {"username": "AlmaUtter_bot", "id": 1}

    result = verify_and_bind("123456:AA-real-looking-token-xx", fetcher=fake_me)
    assert result["ok"] is True
    assert result["username"] == "AlmaUtter_bot"
    assert result["invite"].startswith("https://t.me/AlmaUtter_bot?start=")
    blob = json.dumps(public_status())
    assert "AA-real" not in blob
    assert (tmp_path / "token.txt").read_text().startswith("123456")


def test_start_token_claims_only_matching_chat(monkeypatch, tmp_path):
    monkeypatch.setenv("UTTER_TELEGRAM_STATE", str(tmp_path / "telegram.json"))
    monkeypatch.setenv("UTTER_TELEGRAM_TOKEN_FILE", str(tmp_path / "token.txt"))
    bind_token("123456:AA-real-looking-token-xx", "AlmaUtter_bot")
    token = load_state()["start_token"]
    assert claim_start(99, "fel") is False
    assert is_allowed(99) is False
    assert claim_start(77, token) is True
    assert is_allowed(77) is True
    assert is_allowed(99) is False
