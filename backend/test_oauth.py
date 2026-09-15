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
