"""Kärndemo: frontend + safety. Ingen Ollama, ingen Chroma.

Föräldern ska kunna trycka chips och skriva som barnet
utan att starta Docker. Samma reply_for som /api/preview.
"""

from __future__ import annotations

from pathlib import Path
from uuid import uuid4

from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel

from oauth import catalog, find_local_session, get_provider
from preview import catalog as preview_catalog
from preview import reply_for

ROOT = Path(__file__).resolve().parent.parent
FRONTEND = ROOT / "frontend"

app = FastAPI(title="Gnista kärndemo", version="0.1.0")


class ChatRequest(BaseModel):
    session_id: str | None = None
    message: str


class PreviewTurn(BaseModel):
    message: str


@app.get("/api/health")
async def health():
    return {"status": "ok", "service": "gnista-kernel-demo", "mode": "kernel"}


@app.get("/api/oauth/providers")
async def oauth_providers():
    return {"providers": catalog()}


@app.post("/api/oauth/import/{provider}")
async def oauth_import(provider: str):
    try:
        spec = get_provider(provider)
    except KeyError:
        raise HTTPException(status_code=404, detail="Okänd leverantör.")
    if not spec.get("allowed"):
        raise HTTPException(status_code=403, detail=spec["reason"])
    result = find_local_session(provider)
    if not result.get("ok"):
        raise HTTPException(status_code=404, detail=result["reason"])
    return result


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
    result = reply_for(req.message.strip())
    status = "ok" if result["kind"] in {"socratic", "answer"} else "blocked_input"
    return {
        "session_id": req.session_id or str(uuid4()),
        "response": result["response"],
        "status": status,
        "mode": "kernel",
        "kind": result["kind"],
    }


@app.get("/api/telegram")
async def telegram_status():
    return {
        "username": None,
        "invite": None,
        "linked": False,
        "ready": False,
        "mode": "kernel",
    }


app.mount("/", StaticFiles(directory=str(FRONTEND), html=True), name="frontend")
