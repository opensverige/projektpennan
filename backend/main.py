"""
FastAPI-server. Kör lokalt, exponerar INGET till internet.
"""

from __future__ import annotations

import os
import sys
import uuid
from pathlib import Path

from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel

from pipeline import run_pipeline
from session_store import SessionStore
from reports import list_reports, get_report
from oauth import catalog, find_local_session, get_provider
from preview import catalog as preview_catalog
from preview import reply_for

_here = Path(__file__).resolve().parent
for _root in (_here.parent, _here):
    if (_root / "skooli_buddy").is_dir() and str(_root) not in sys.path:
        sys.path.append(str(_root))

from skooli_buddy.telegram_link import public_status, verify_and_bind

app = FastAPI(title="Skooli Buddy", version="0.2.0")

VAULT_PATH = Path(os.getenv("VAULT_PATH", "/app/vault"))
SESSION_DB_PATH = VAULT_PATH / "session-store.db"

session_store = SessionStore(SESSION_DB_PATH)


class ChatRequest(BaseModel):
    session_id: str | None = None
    message: str


class ChatResponse(BaseModel):
    session_id: str
    response: str
    status: str


@app.post("/api/chat", response_model=ChatResponse)
async def chat(req: ChatRequest):
    if not req.message or not req.message.strip():
        raise HTTPException(status_code=400, detail="Tomt meddelande.")

    if len(req.message) > 1000:
        raise HTTPException(status_code=400, detail="Meddelandet är för långt (max 1000 tecken).")

    session_id = req.session_id or str(uuid.uuid4())

    history = session_store.get_history(session_id)

    result = await run_pipeline(session_id, req.message.strip(), history)

    if result["status"] == "ok":
        history.append({"role": "user", "content": req.message.strip()})
        history.append({"role": "assistant", "content": result["response"]})
        if len(history) > 40:
            history[:] = history[-40:]
        session_store.save_history(session_id, history)

    return ChatResponse(
        session_id=session_id,
        response=result["response"],
        status=result["status"]
    )


@app.get("/api/health")
async def health():
    return {"status": "ok", "service": "skooli-buddy", "version": "0.2.0"}


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


class PreviewTurn(BaseModel):
    message: str


@app.get("/api/preview")
async def preview_index():
    return preview_catalog()


@app.post("/api/preview/turn")
async def preview_turn(req: PreviewTurn):
    if not req.message or not req.message.strip():
        raise HTTPException(status_code=400, detail="Tomt meddelande.")
    return reply_for(req.message.strip())


class TelegramBind(BaseModel):
    token: str


@app.get("/api/telegram")
async def telegram_status():
    return public_status()


@app.post("/api/telegram/bind")
async def telegram_bind(req: TelegramBind):
    try:
        return verify_and_bind(req.token)
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc


@app.get("/api/reports")
async def reports_index():
    return {"reports": list_reports()}


@app.get("/api/reports/{report_id}")
async def reports_detail(report_id: str):
    report = get_report(report_id)
    if not report:
        raise HTTPException(status_code=404, detail="Rapporten hittades inte.")
    return report


app.mount("/", StaticFiles(directory="/app/frontend", html=True), name="frontend")
