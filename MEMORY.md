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

## 2026-09-15 — produktifiering
- Mall: Accounted Open/Auto/Custom + Odysseus BYO.
- Hem-barn är en tyst WhatsApp-kontakt, inte QR/PWA-ceremoni.
- Föräldern sätter upp utan barnet i rummet. Inget läxpush.
- Hosted = vi blir personuppgiftsansvariga → DPIA innan sälj.
- Docs: PRODUCTIZATION.md, PRICING.md. Backlog P-25–P-32.

## 2026-09-15 — förälderns kernel
- Lgr22 är valfritt pack, inte överhet. Världsbild (inklusive tro)
  är förälderns. Egna agenter. Flera metoder utöver Sokrates.
- Diagnos/preferenser bara om föräldern skrivit dem; tyst anpassning.
  Tomt = extra-stöd-default. Art. 9 i Hem (P-36).
- Docs: PLATFORM.md. Pack-skelett i `vault/packs/`. Tutorregler v3.
- Backlog P-33–P-36. Research: parent-sovereignty-kernel,
  pedagogy-beyond-socratic, parent-authored-accommodations.
- Namnet är låst som rekommendation: kontakt **Gnista**, initiativ Projekt Pennan. Se `docs/NAME.md`. Skooli Buddy fasas (P-40).
- Plattan: vi ger safety/vault/ytor. Föräldern jackar in modell (ChatGPT m.fl.). Onboarding börjar på `frontend/start.html`. Se `docs/BASEPLATE.md`.

## 2026-09-15 — byggarföräldrar + skolkontext
- Analog: Obsidian-vault + Odysseus-runtime. Vi standardiserar
  det de redan bygger. Skolan aldrig operatör.
- Skolkontext = förälder-ägd, minimerad (ämne/tema, TTL).
  Connector hos dem, lösen aldrig till Hem. P-37, P-38.
- Research: parent-owned-school-context. Öppna skolplattformen
  är beviset att de redan gör ingest själva.

## 2026-09-15 — install vs monument
- Hem-onboarding är ritad, inte kod. `docs/INSTALL.md` håller
  isär Open-kväll (Docker / Telegram `/consent`) och Hem
  (BankID + tyst kontakt, P-28). Ingen barn-onboarding, avsiktligt.
