"""Live SOUL-demo: frontend + tutorfiler + Ollama.

Läxa går till modellen. Kris/block stannar i koden.
"""

from __future__ import annotations

from uuid import uuid4

from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel

from preview import catalog as preview_catalog
from preview import reply_for
from soul import MODEL_NAME, ollama_up, turn

from demo import FRONTEND

app = FastAPI(title="Gnista SOUL", version="0.1.0")

_sessions: dict[str, list[dict]] = {}


class ChatRequest(BaseModel):
    session_id: str | None = None
    message: str


class PreviewTurn(BaseModel):
    message: str


@app.get("/api/health")
async def health():
    live = await ollama_up()
    return {
        "status": "ok" if live else "degraded",
        "service": "gnista-soul",
        "mode": "soul",
        "model": MODEL_NAME,
        "ollama": live,
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
async def chat(req: ChatRequest):
    if not req.message or not req.message.strip():
        raise HTTPException(status_code=400, detail="Tomt meddelande.")
    session_id = req.session_id or str(uuid4())
    history = _sessions.setdefault(session_id, [])
    result = await turn(req.message, history)
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
