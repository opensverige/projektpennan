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
- `pipeline.py` orchestrerar, `safety.py` kör deterministiska filter.
- `session_store.py` + SQLite (`vault/session-store.db`) håller chatthistorik.
- `rag.py` använder Chroma + Ollama-embeddings (`nomic-embed-text`) och läser data från `vault/curriculum-vectors/`.
- `reports.py` exponerar `/api/reports` (guardian dashboard) baserat på `vault/parent-reports/*.json`.
- Miljövariabler: `OLLAMA_URL` (default `http://ollama:11434`), `MODEL_NAME` (default `hermes3:8b`), `EMBED_MODEL` (default `nomic-embed-text`).
- Auditlogg i `vault/audit/audit.log` är kedjad + HMAC-signad (hemlighet i `vault/config/audit-secret.txt`).

### Frontend
- `frontend/index.html` är elevchatten och länkar till `guardian.html` (föräldravyn med rapportlista).

### Vault
- `vault/config/child-profile.json` + `policies.json` måste finnas innan start.
- `vault/curriculum-vectors/` innehåller JSON/JSONL med kursplansutdrag + `chroma/` för index.
- `vault/parent-reports/` lagrar JSON-rapporter som frontenden visar.
- `vault/conversations/` och `vault/audit/` växer utan rotation, planerat att adresseras i fas 2.

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
- Fyll `vault/curriculum-vectors/` med Lgr22-data + CLI för uppdatering.
- Utöka guardian dashboard med auth + export.
- Rotera/logga `vault/conversations/` och `vault/audit/` (arkivering).
