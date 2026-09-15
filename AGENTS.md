# Skooli Buddy — Agent Brief

## Mission
Föräldrastyrd AI-studiekompis för barn i åk 4–6 (mål: åk 1–9).
Barnet får en sidekick som hjälper till att tänka, öva och orka — inte en
läxmaskin som ger svar. Föräldern sitter i spakarna. Skolans system är
aldrig operatör, datavärd eller beslutsfattare.

Projektet är öppen källkod under [opensverige](https://opensverige.se)
(AGPL-3.0). Ingen elevdata ska behöva lämna hemmet för att produkten
ska fungera.

## Icke-förhandlingsbara principer
1. **Föräldern styr.** Samtycke, paus, radering, tidsgränser, stödläge,
   världsbild, packs och insyn är vårdnadshavarens. Skola, kommun,
   läroplan eller leverantör får inte kopplas in som kontrollplan.
   Skolan får vara källa bara via förälder-ägd, minimerad kontext.
2. **Koden validerar. Modellen undervisar.** Säkerhet, samtycke och
   gränser ligger i kod — inte i en prompt. Packs kan inte stänga av
   safety-kärnan.
3. **Ge aldrig svaret först.** Flera metoder (Sokrates, små steg,
   worked, CPA, saga, lek). Extra stöd är default. Inget läx-nudge.
4. **Dataminimering.** Numeriskt id, aldrig namn/adress/skol-id.
   Lokal lagring. `/revoke` raderar allt. Diagnosanteckningar och
   skolkontext är valfria och extra skyddade. Inga klasslistor.
5. **Öppenhet / ingen vendor lock-in.** Kernel + packs som filer.
   Föräldern kan exportera, köra hemma, ladda egna agenter. Inga
   hemliga barn-profiler i git.

## Source of Truth
| Yta | Sanning |
|-----|---------|
| Identitet & pedagogik | `agents/tutor/SOUL.md` + `SKILL.md` + `RULES.md` |
| Säkerhetsspec | `SKOOLI_BUDDY_SAFETY_SPEC.md` |
| Produktvision | `docs/PRODUCT.md` + `docs/PRODUCTIZATION.md` + `docs/PLATFORM.md` + `docs/UX-SCENARIOS.md` |
| Vad som är byggt | `docs/INVENTORY.md` |
| Vad som ska göras | `docs/BACKLOG.md` |
| Research | `research/` + `scripts/research_pipeline.py` |
| Lokal stack-flöde | `backend/pipeline.py` |
| Telegram-stack | `skooli_buddy/` |

Prompten ska **laddas från SOUL/SKILL/RULES**, inte dupliceras i
Python. `skooli_buddy/core.py` bryter mot det idag — se backlog P-01.

## Två stackar (tillfälligt)
Repot har två parallella implementationer. Båda är verkliga. Ingen får
raderas tyst. Målet är **en kärna, två ytor**.

```
Kärna (målbild)
  profil + policies + packs + safety + logg + research-fynd
        │
        ├─ Yta A: FastAPI + lokal Ollama + HTML-chat + vault/
        └─ Yta B: Telegram-bot + valfri moln-LLM + Streamlit-dashboard
```

| | Yta A — hem/lokal | Yta B — messaging |
|---|-------------------|-------------------|
| Kod | `backend/`, `frontend/`, `vault/`, `agents/` | `skooli_buddy/`, `dashboard/`, `config/` |
| Modell | Ollama (`hermes3:8b`) | Gemini 2.5 Flash |
| Data | `vault/` (SQLite, HMAC-audit, Chroma) | `logs/*.jsonl`, `config/consents.json` |
| UI | `frontend/index.html` + `guardian.html` | Telegram + Streamlit |
| Status | Scaffold med RAG + audit | Live-testad mot barn, 12 enhetstester |

**Default för OSS-release:** lokal-först (Yta A). Gemini är
utvecklingsgenväg, inte produktkrav. Föräldern ska kunna köra
helt offline.

## Vault
Lämna katalogstrukturen orörd: `config/`, `conversations/`, `audit/`,
`curriculum-vectors/`, `parent-reports/`, `packs/`. Testprofilen
"Test-Elev" får ligga kvar. Riktiga barnprofiler och ifyllda
världsbilds-/diagnos-packs committas aldrig.

## Development Workflow
```bash
# Lokal stack
docker compose up --build          # http://localhost:8080
# eller: uvicorn main:app --reload --host 0.0.0.0 --port 8080   (från backend/)

# Telegram-stack
cp .env.example .env
python -m skooli_buddy.bot
streamlit run dashboard/app.py

# Tester + research
python -m pytest tests/ -v
python scripts/research_pipeline.py validate
python scripts/curriculum_cli.py validate
```

## Safety
- Utöka mönster i `backend/safety.py` och följ
  `SKOOLI_BUDDY_SAFETY_SPEC.md`. Lägg inte nya hårda regler bara i
  modellen.
- Svenska + engelska blockmönster. Hänvisa till BRIS 116 111 vid
  allvarliga signaler — koden ska kunna tvinga det, inte bara prompten.
- Ingen utåt-nätverk för lokal backend utöver Ollama.
- Hardcoded `ALLOWED_CHAT_ID` i `skooli_buddy/bot.py` är en
  utvecklingslåsning, inte en OSS-default.

## Current Focus
1. En kärna, BYO-providers (P-01, P-26).
2. Safety i kod + allowlist/start-token (P-03, P-30).
3. WhatsApp-kontakt hos barnet, förälder-PWA hos vuxen (P-32, P-27).
   Inte sälj Hem innan DPIA (P-29). Inget QR-ceremoni.
4. Productisering: `docs/PRODUCTIZATION.md` är affärsmodellen.
   `docs/PLATFORM.md` är kernel/pack-gränsen. Arbetsnamn.
5. Pack-laddare (P-33), världsbild (P-34), metoder i kod (P-35),
   krypterade anpassningar (P-36), förälder-ägd skolkontext (P-37,
   P-38). Lgr22 åk 4–6 som pack.
