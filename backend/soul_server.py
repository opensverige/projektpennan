"""Live SOUL-demo: frontend + tutorfiler + BYO-modell.

Läxa går till frontier/smart OSS. Kris/block stannar i koden.
"""

from __future__ import annotations

from uuid import uuid4

from fastapi import FastAPI, Header, HTTPException
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel

from preview import catalog as preview_catalog
from preview import reply_for
from providers import load_runtime, ping, ready
from soul import turn

from demo import FRONTEND

app = FastAPI(title="Utter SOUL", version="0.2.0")

_sessions: dict[str, list[dict]] = {}


class ChatRequest(BaseModel):
    session_id: str | None = None
    message: str


class PreviewTurn(BaseModel):
    message: str


@app.get("/api/health")
async def health():
    runtime = load_runtime()
    live = await ping(runtime)
    return {
        "status": "ok" if live else "degraded",
        "service": "utter-soul",
        "mode": "soul",
        "model": runtime.label() if ready(runtime) else None,
        "provider": runtime.provider,
    }


@app.get("/api/preview")
async def preview_index():
    return preview_catalog()


@app.post("/api/preview/turn")
async def preview_turn(req: PreviewTurn):
    if not req.message or not req.message.strip():
        raise HTTPException(status_code=400, detail="Tomt meddelande.")
    return reply_for(req.message.strip())


@app.post("/api/chat")
async def chat(
    req: ChatRequest,
    x_utter_key: str | None = Header(default=None),
    x_utter_provider: str | None = Header(default=None),
):
    if not req.message or not req.message.strip():
        raise HTTPException(status_code=400, detail="Tomt meddelande.")
    session_id = req.session_id or str(uuid4())
    history = _sessions.setdefault(session_id, [])
    result = await turn(
        req.message,
        history,
        api_key=x_utter_key,
        provider=x_utter_provider,
    )
    if result["status"] == "ok":
        history.append({"role": "user", "content": req.message.strip()})
        history.append({"role": "assistant", "content": result["response"]})
        if len(history) > 40:
            _sessions[session_id] = history[-40:]
    return {
        "session_id": session_id,
        "response": result["response"],
        "status": result["status"],
        "mode": "soul",
        "kind": result.get("kind"),
        "model": result.get("model"),
    }


@app.get("/api/telegram")
async def telegram_status():
    return {"username": None, "invite": None, "linked": False, "ready": False}


app.mount("/", StaticFiles(directory=str(FRONTEND), html=True), name="frontend")
