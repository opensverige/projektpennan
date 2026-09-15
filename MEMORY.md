# Project Memory — Skooli Buddy

## 2026-03-11
- Repo förberedd för GitHub (AGENTS.md + MEMORY.md skapade).
- Docker Compose kör FastAPI + frontend, kräver lokal Ollama på port 11434.
- Vault innehåller testprofil "Test-Elev" och policies scaffolding.
- Kommande arbetsordning: (1) implementera Chroma-baserad RAG, (2) flytta sessionstore till SQLite, (3) bygga guardian-dashboard över `vault/parent-reports`.

## 2026-03-12
- Sessionhistorik flyttad till SQLite (`backend/session_store.py` + `vault/session-store.db`) och kopplad i `backend/main.py`. RAM-store är borta.
- RAG aktiverat med Chroma + Ollama (`backend/rag.py`) och sampledata i `vault/curriculum-vectors/sample-lgr22.json`.
- Guardian dashboard exponerar `/api/reports` + `frontend/guardian.html`; audit-logg signeras med HMAC-sekret i `vault/config/audit-secret.txt`.

## 2026-03 — Telegram-spåret
- Yta B: `skooli_buddy/` + Streamlit-dashboard + Gemini 2.5 Flash.
- GDPR-consent, JSONL-logg, persona-matris, ett barntest.
- README skrevs om mot Telegram; AGENTS.md blev kvar på FastAPI.

## 2026-09-15
- Inventering: två halva produkter, föräldern styr bara delvis.
- Vision låst: hemverktyg, inte skolsystem. Extra stöd som default.
- Regler v2 i SOUL/SKILL/RULES + SAFETY_SPEC. Research-pipeline i
  `research/` med 8 accepted-fynd. Backlog P-01–P-24 i `docs/BACKLOG.md`.
- Policies fick `parent_controls` + stödlägen. Profilen fick
  `support_preferences` (inga diagnoser).
