import json

from oauth import catalog, find_local_session, get_provider


def test_chatgpt_and_grok_allowed_claude_forbidden():
    by_id = {p["id"]: p for p in catalog()}
    assert by_id["chatgpt"]["allowed"] is True
    assert by_id["grok"]["allowed"] is True
    assert by_id["claude"]["allowed"] is False
    assert "API-nyckel" in by_id["claude"]["reason"]


def test_claude_has_no_device_url():
    spec = get_provider("claude")
    assert spec["allowed"] is False
    assert "device_url" not in spec


def test_missing_local_session_is_honest():
    result = find_local_session("chatgpt")
    assert result["ok"] is False
    assert "länken" in result["reason"]


def test_claude_import_stays_forbidden():
    result = find_local_session("claude")
    assert result["ok"] is False
    assert "API-nyckel" in result["reason"]


def test_import_never_returns_tokens(tmp_path):
    codex = tmp_path / ".codex"
    codex.mkdir()
    (codex / "auth.json").write_text(
        json.dumps(
            {
                "access_token": "secret-token-xyz",
                "refresh_token": "refresh-secret",
            }
        ),
        encoding="utf-8",
    )
    result = find_local_session("chatgpt", home=tmp_path)
    assert result["ok"] is True
    assert result["provider"] == "chatgpt"
    blob = json.dumps(result)
    assert "secret-token" not in blob
    assert "refresh-secret" not in blob
    assert set(result) <= {"ok", "provider", "source"}


def test_hermes_grok_does_not_count_as_chatgpt(tmp_path):
    hermes = tmp_path / ".hermes"
    hermes.mkdir()
    (hermes / "auth.json").write_text(
        json.dumps(
            {
                "xai-oauth": {
                    "access_token": "grok-only-token",
                    "refresh_token": "grok-refresh",
                }
            }
        ),
        encoding="utf-8",
    )
    assert find_local_session("chatgpt", home=tmp_path)["ok"] is False
    grok = find_local_session("grok", home=tmp_path)
    assert grok["ok"] is True
    assert "grok-only-token" not in json.dumps(grok)
