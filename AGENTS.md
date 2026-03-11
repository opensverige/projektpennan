# Skooli Buddy — Agent Brief

## Mission
AI-stödd studiekompis för mellanstadiet (åk 4–6) som kör helt lokalt. FastAPI-backend pratar med Ollama i LAN, statisk HTML-chat UI. Ingen molnkoppling, inga elevdata lämnar datorn.

## Source of Truth
- `agents/tutor/SOUL.md` + `SKILL.md` + `RULES.md` definierar lärarpersonan och beteenden. Backend staplar dem i en prompt tillsammans med barnets profil och policyer från `vault/config/`.
- `backend/pipeline.py` är den enda sanningen för flödet (preflight → safety → RAG placeholder → LLM → safety → logg → svar).
- `vault/` innehåller all data (barnprofil, policies, konversationsloggar, auditkedja, framtida RAG-embeddings). Lämna katalogstrukturen orörd.

## Architecture Overview
```
Docker (uvicorn) ─┬─ FastAPI (`backend/main.py`)
                  │    └─ `run_pipeline()` (input grinder + LLM call)
                  ├─ Static frontend (`frontend/index.html`)
                  └─ Bind mounts: `vault/`, `agents/`, `frontend/`
```

### Backend
- Python 3.11 + FastAPI 0.115, uvicorn worker.
- `pipeline.py` orchestrerar, `safety.py` kör deterministiska filter, `rag.py` är scaffold för kommande Chroma.
- Miljövariabler: `OLLAMA_URL` (default `http://ollama:11434`), `MODEL_NAME` (default `hermes3:8b`).
- Alla loggar (conversations + audit hashkedja) hamnar i `vault/` och är append-only.

### Frontend
- Enkel statisk chat i `frontend/index.html`; inbyggd CSS/JS. Pratar mot `/api/chat` och visar block/error-meddelanden.

### Vault
- `vault/config/child-profile.json` + `policies.json` måste finnas innan start.
- `vault/curriculum-vectors/` reserverad för RAG (fas 2).
- `vault/conversations/` och `vault/audit/` växer utan rotation, planerat åtgärdas i fas 2.

## Development Workflow
1. Kör Ollama lokalt med modellen du vill testa (`ollama run hermes3:8b`).
2. Starta stacken:
   ```bash
   cd skooli-buddy
   docker compose up --build
   ```
3. Öppna http://localhost:8080 i webbläsare.
4. För backend-only dev: `uvicorn main:app --reload --host 0.0.0.0 --port 8080` från `backend/` (kräver `pip install -r backend/requirements.txt`).
5. Vault-filer mountas, så uppdatera `vault/config` lokalt och starta om containern vid behov.

## Safety & Compliance Notes
- Ingen nätverksåtkomst utåt för backend (förutom Ollama localhost). Behåll det så.
- LLM gör undervisning, men koden bestämmer om input/output får passera. Utöka mönsterlistan i `safety.py` istället för att lägga regler i modellen.
- Elevdata ska anonymiseras i `child-profile.json`. Testprofilen "Test-Elev" får ligga kvar i repo.

## Current Focus / Next Steps
- Implementera riktig RAG mot Lgr22 (`rag.py`).
- Flytta session store till SQLite (just nu ligger allt i RAM i `main.py`).
- Lägg till guardian dashboard (föräldrarapporter finns som stubbar i `vault/parent-reports`).
- Utöka auditkedjan med signatur när databas finns.
