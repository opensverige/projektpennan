"""
FastAPI-server. Kör lokalt, exponerar INGET till internet.
"""

from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pydantic import BaseModel
import uuid

from pipeline import run_pipeline

app = FastAPI(title="Skooli Buddy", version="0.1.0")

# In-memory session store (ersätts med SQLite i nästa fas)
sessions: dict[str, list[dict]] = {}


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

    # Max message length (barn ska inte kunna pasta in uppsatser)
    if len(req.message) > 1000:
        raise HTTPException(status_code=400, detail="Meddelandet är för långt (max 1000 tecken).")

    session_id = req.session_id or str(uuid.uuid4())

    if session_id not in sessions:
        sessions[session_id] = []

    history = sessions[session_id]

    result = await run_pipeline(session_id, req.message.strip(), history)

    # Uppdatera historik (behåll senaste 20 meddelanden)
    if result["status"] == "ok":
        history.append({"role": "user", "content": req.message.strip()})
        history.append({"role": "assistant", "content": result["response"]})
        # Sliding window
        if len(history) > 40:
            history[:] = history[-40:]

    return ChatResponse(
        session_id=session_id,
        response=result["response"],
        status=result["status"]
    )


@app.get("/api/health")
async def health():
    return {"status": "ok", "service": "skooli-buddy", "version": "0.1.0"}


# Serve frontend
app.mount("/", StaticFiles(directory="/app/frontend", html=True), name="frontend")
