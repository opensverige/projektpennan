"""BYO-modell. Frontier eller smart OSS. Ollama bara om föräldern valt det.

Nyckeln ligger i miljön, i runtime.json:s env-namn, eller i
X-Utter-Key från den lokala starten. Den loggas inte.
"""

from __future__ import annotations

import json
import os
from pathlib import Path

import httpx

ROOT = Path(__file__).resolve().parent.parent
VAULT = Path(os.getenv("VAULT_PATH", ROOT / "vault"))

# OpenAI-kompatibla först. Anthropic har egen form.
_OPENAI_STYLE = {
    "openai": {
        "base_url": "https://api.openai.com/v1",
        "model": "gpt-4.1-mini",
        "key_env": "OPENAI_API_KEY",
    },
    "chatgpt": {
        "base_url": "https://api.openai.com/v1",
        "model": "gpt-4.1-mini",
        "key_env": "OPENAI_API_KEY",
    },
    "xai": {
        "base_url": "https://api.x.ai/v1",
        "model": "grok-3-mini",
        "key_env": "XAI_API_KEY",
    },
    "grok": {
        "base_url": "https://api.x.ai/v1",
        "model": "grok-3-mini",
        "key_env": "XAI_API_KEY",
    },
    "groq": {
        "base_url": "https://api.groq.com/openai/v1",
        "model": "llama-3.3-70b-versatile",
        "key_env": "GROQ_API_KEY",
    },
    "gemini": {
        "base_url": "https://generativelanguage.googleapis.com/v1beta/openai",
        "model": "gemini-2.0-flash",
        "key_env": "GEMINI_API_KEY",
    },
}

_DETECT = (
    ("openai", "OPENAI_API_KEY"),
    ("xai", "XAI_API_KEY"),
    ("anthropic", "ANTHROPIC_API_KEY"),
    ("groq", "GROQ_API_KEY"),
    ("gemini", "GEMINI_API_KEY"),
)


class Runtime:
    def __init__(
        self,
        provider: str,
        model: str,
        base_url: str | None,
        api_key: str | None,
    ):
        self.provider = provider
        self.model = model
        self.base_url = (base_url or "").rstrip("/")
        self.api_key = api_key

    def label(self) -> str:
        return f"{self.provider}:{self.model}"


def _runtime_file() -> dict:
    path = VAULT / "config" / "runtime.json"
    if not path.is_file():
        return {}
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return {}
    return data if isinstance(data, dict) else {}


def detect_provider() -> str | None:
    for name, env in _DETECT:
        if os.getenv(env, "").strip():
            return name
    if os.getenv("OPENAI_BASE_URL", "").strip():
        return "openai-compat"
    if os.getenv("OLLAMA_URL", "").strip() or os.getenv("MODEL_NAME", "").strip():
        return "ollama"
    return None


def load_runtime(
    override_key: str | None = None,
    override_provider: str | None = None,
) -> Runtime:
    data = _runtime_file()
    provider = (
        (override_provider or "").strip()
        or (data.get("provider") or "").strip()
        or detect_provider()
        or ""
    )
    if provider in ("chatgpt-oauth",):
        provider = "chatgpt"
    if provider in ("grok-oauth",):
        provider = "grok"
    if provider == "local":
        provider = detect_provider() or ""

    spec = _OPENAI_STYLE.get(provider, {})
    model = (
        (data.get("model") or "").strip()
        or os.getenv("MODEL_NAME", "").strip()
        or spec.get("model")
        or "gpt-4.1-mini"
    )
    base = (
        (data.get("base_url") or "").strip()
        or os.getenv("OPENAI_BASE_URL", "").strip()
        or spec.get("base_url")
    )
    key_env = data.get("api_key_env") or spec.get("key_env")
    key = (override_key or "").strip() or (
        os.getenv(key_env, "").strip() if key_env else ""
    )
    if provider == "anthropic":
        key = key or os.getenv("ANTHROPIC_API_KEY", "").strip()
        model = (
            (data.get("model") or "").strip()
            or os.getenv("MODEL_NAME", "").strip()
            or "claude-sonnet-4-5"
        )
        base = (data.get("base_url") or "").strip() or "https://api.anthropic.com"
    if provider == "ollama":
        base = (
            (data.get("base_url") or "").strip()
            or os.getenv("OLLAMA_URL", "").strip()
            or "http://127.0.0.1:11434"
        )
        model = (
            (data.get("model") or "").strip()
            or os.getenv("MODEL_NAME", "").strip()
            or "llama3.2:3b"
        )
        key = None
    if provider == "openai-compat" and not base:
        base = os.getenv("OPENAI_BASE_URL", "").strip()
        key = key or os.getenv("OPENAI_API_KEY", "").strip() or "local"
    return Runtime(provider or "none", model, base, key or None)


def ready(runtime: Runtime | None = None) -> bool:
    rt = runtime or load_runtime()
    if rt.provider in ("none", ""):
        return False
    if rt.provider == "ollama":
        return bool(rt.base_url)
    if rt.provider == "anthropic":
        return bool(rt.api_key)
    if rt.provider == "openai-compat":
        return bool(rt.base_url)
    return bool(rt.api_key and rt.base_url)


async def complete(
    system_prompt: str,
    history: list[dict],
    runtime: Runtime | None = None,
) -> str:
    rt = runtime or load_runtime()
    if not ready(rt):
        raise RuntimeError(
            "Ingen modell. Klistra en nyckel (ChatGPT, Grok, Claude, Groq) "
            "eller peka OPENAI_BASE_URL mot en lokal motor."
        )
    if rt.provider == "ollama":
        return await _ollama(rt, system_prompt, history)
    if rt.provider == "anthropic":
        return await _anthropic(rt, system_prompt, history)
    return await _openai_compat(rt, system_prompt, history)


async def _openai_compat(rt: Runtime, system_prompt: str, history: list[dict]) -> str:
    messages = [{"role": "system", "content": system_prompt}, *history]
    headers = {"Content-Type": "application/json"}
    if rt.api_key and rt.api_key != "local":
        headers["Authorization"] = f"Bearer {rt.api_key}"
    async with httpx.AsyncClient(timeout=120.0) as client:
        response = await client.post(
            f"{rt.base_url}/chat/completions",
            headers=headers,
            json={
                "model": rt.model,
                "messages": messages,
                "temperature": 0.7,
                "max_tokens": 512,
            },
        )
        response.raise_for_status()
        data = response.json()
    return (
        (((data.get("choices") or [{}])[0].get("message") or {}).get("content")) or ""
    ).strip()


async def _anthropic(rt: Runtime, system_prompt: str, history: list[dict]) -> str:
    converted = []
    for item in history:
        role = item.get("role")
        if role not in ("user", "assistant"):
            continue
        converted.append({"role": role, "content": item.get("content") or ""})
    async with httpx.AsyncClient(timeout=120.0) as client:
        response = await client.post(
            f"{rt.base_url}/v1/messages",
            headers={
                "Content-Type": "application/json",
                "x-api-key": rt.api_key or "",
                "anthropic-version": "2023-06-01",
            },
            json={
                "model": rt.model,
                "max_tokens": 512,
                "system": system_prompt,
                "messages": converted or [{"role": "user", "content": "Hej"}],
            },
        )
        response.raise_for_status()
        data = response.json()
    parts = data.get("content") or []
    text = "".join(p.get("text") or "" for p in parts if isinstance(p, dict))
    return text.strip()


async def _ollama(rt: Runtime, system_prompt: str, history: list[dict]) -> str:
    messages = [{"role": "system", "content": system_prompt}, *history]
    async with httpx.AsyncClient(timeout=120.0) as client:
        response = await client.post(
            f"{rt.base_url}/api/chat",
            json={
                "model": rt.model,
                "messages": messages,
                "stream": False,
                "options": {"temperature": 0.7, "num_predict": 512},
            },
        )
        response.raise_for_status()
        data = response.json()
    return ((data.get("message") or {}).get("content") or "").strip()


async def ping(runtime: Runtime | None = None) -> bool:
    rt = runtime or load_runtime()
    if not ready(rt):
        return False
    if rt.provider == "ollama":
        try:
            async with httpx.AsyncClient(timeout=2.0) as client:
                res = await client.get(f"{rt.base_url}/api/tags")
            return res.status_code == 200
        except httpx.HTTPError:
            return False
    return True
