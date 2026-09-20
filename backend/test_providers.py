import asyncio

import json

from providers import complete, detect_provider, load_runtime, ready


def test_detects_openai_before_ollama(monkeypatch):
    monkeypatch.setenv("OPENAI_API_KEY", "sk-test")
    monkeypatch.setenv("OLLAMA_URL", "http://127.0.0.1:11434")
    assert detect_provider() == "openai"
    rt = load_runtime()
    assert rt.provider == "openai"
    assert rt.model == "gpt-4.1-mini"
    assert ready(rt)


def test_groq_is_smart_oss(monkeypatch):
    monkeypatch.delenv("OPENAI_API_KEY", raising=False)
    monkeypatch.setenv("GROQ_API_KEY", "gsk_test")
    rt = load_runtime()
    assert rt.provider == "groq"
    assert "llama" in rt.model
    assert rt.base_url.startswith("https://api.groq.com")


def test_no_model_is_not_ready(monkeypatch):
    for name in (
        "OPENAI_API_KEY",
        "XAI_API_KEY",
        "ANTHROPIC_API_KEY",
        "GROQ_API_KEY",
        "GEMINI_API_KEY",
        "OPENAI_BASE_URL",
        "OLLAMA_URL",
        "MODEL_NAME",
    ):
        monkeypatch.delenv(name, raising=False)
    rt = load_runtime()
    assert rt.provider == "none"
    assert not ready(rt)


def test_imported_chatgpt_session_is_the_key(tmp_path, monkeypatch):
    for name in (
        "OPENAI_API_KEY",
        "XAI_API_KEY",
        "ANTHROPIC_API_KEY",
        "GROQ_API_KEY",
        "GEMINI_API_KEY",
        "OPENAI_BASE_URL",
        "OLLAMA_URL",
        "MODEL_NAME",
    ):
        monkeypatch.delenv(name, raising=False)
    monkeypatch.setattr("oauth.VAULT", tmp_path)
    (tmp_path / "config").mkdir()
    (tmp_path / "config" / "oauth-session.json").write_text(
        json.dumps({"provider": "chatgpt", "access_token": "codex-live", "source": "~/.codex/auth.json"}),
        encoding="utf-8",
    )
    rt = load_runtime(override_provider="chatgpt")
    assert rt.provider == "chatgpt"
    assert rt.api_key == "codex-live"
    assert ready(rt)


def test_header_key_overrides_env(monkeypatch):
    monkeypatch.setenv("OPENAI_API_KEY", "sk-env")
    rt = load_runtime(override_key="sk-header", override_provider="xai")
    assert rt.provider == "xai"
    assert rt.api_key == "sk-header"
    assert "x.ai" in rt.base_url


def test_openai_compat_posts_chat_completions(monkeypatch):
    captured = {}

    class FakeResp:
        def raise_for_status(self):
            return None

        def json(self):
            return {"choices": [{"message": {"content": "Vad är 7×7?"}}]}

    class FakeClient:
        def __init__(self, *args, **kwargs):
            pass

        async def __aenter__(self):
            return self

        async def __aexit__(self, *args):
            return False

        async def post(self, url, headers=None, json=None):
            captured["url"] = url
            captured["headers"] = headers
            captured["json"] = json
            return FakeResp()

    monkeypatch.setattr("providers.httpx.AsyncClient", FakeClient)
    rt = load_runtime(override_key="sk-test", override_provider="openai")
    reply = asyncio.run(complete("Du är Utter.", [{"role": "user", "content": "7*8"}], rt))
    assert reply == "Vad är 7×7?"
    assert captured["url"].endswith("/chat/completions")
    assert captured["headers"]["Authorization"] == "Bearer sk-test"
    assert captured["json"]["messages"][0]["role"] == "system"


def test_openai_compat_sends_photo_on_last_user(monkeypatch):
    captured = {}

    class FakeResp:
        def raise_for_status(self):
            return None

        def json(self):
            return {"choices": [{"message": {"content": "Vad syns i bråket?"}}]}

    class FakeClient:
        def __init__(self, *args, **kwargs):
            pass

        async def __aenter__(self):
            return self

        async def __aexit__(self, *args):
            return False

        async def post(self, url, headers=None, json=None):
            captured["json"] = json
            return FakeResp()

    monkeypatch.setattr("providers.httpx.AsyncClient", FakeClient)
    rt = load_runtime(override_key="sk-test", override_provider="openai")
    reply = asyncio.run(
        complete(
            "Du är Utter.",
            [{"role": "user", "content": "foto av läxan"}],
            rt,
            image="abc123",
            image_mime="image/jpeg",
        )
    )
    assert reply == "Vad syns i bråket?"
    content = captured["json"]["messages"][-1]["content"]
    assert content[0]["text"] == "foto av läxan"
    assert content[1]["image_url"]["url"].startswith("data:image/jpeg;base64,abc123")
