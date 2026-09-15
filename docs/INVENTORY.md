# Inventering — vad som är byggt

Datum: 2026-09-15. Underlag: kod på `main` + research-pass.
Uppdatera den här filen när en yta ändrar status, inte när en
prompt-rad tweakas.

## Sammanfattning
Vi har en **fungerande Telegram-sidekick** med samtycke, Sokratisk
prompt, Lgr22-stubb och en enkel föräldralogg — plus en **äldre
lokal FastAPI-stack** med RAG, HMAC-audit och HTML-chat. De två
stackarna delar inte kärna. Regler och README pekade åt olika håll
tills den här branchen.

Produkten är ett lovande MVP mot ett barn, inte en OSS-release.

```
Betyg (0–5)
  Pedagogik i prompt          ████░  4
  Pedagogik i kod             ██░░░  2
  Föräldern i spakarna        ██░░░  2
  Extra stöd / UDL            █░░░░  1
  Lgr22-täckning              █░░░░  1
  Safety i kod                ██░░░  2
  Integritet / GDPR-skelett   ███░░  3
  Lokal-först                 ██░░░  2
  OSS-hygien                  ██░░░  2
  Research-loop               █░░░░  1 → den här branchen: 3
```

## Yta B — Telegram + Gemini (det README säljer)

| Del | Fil | Status |
|-----|-----|--------|
| Bot + kommandon | `skooli_buddy/bot.py` | `/start /consent /revoke /reset /help`. Ingen `/pause` trots att samtyckestexten lovar den. |
| Hjärna | `skooli_buddy/core.py` | Gemini 2.5 Flash, 13 regler i en hårdkodad prompt, 20 turer i RAM. |
| Samtycke | `skooli_buddy/consent.py` | JSON-fil, timestamp, revoke + `pending_deletion`. |
| Logg | `skooli_buddy/logger.py` | GDPR-minimerad JSONL per dag. |
| Profil | `skooli_buddy/profile.py` | Läser `config/child_profile.json` + hela `config/lgr22/*.json` rakt in i prompten. Ingen RAG. |
| Dashboard | `dashboard/app.py` | Streamlit + lösenord. Visar räknare. **Läser fälten `user`/`bot` men loggen skriver `user_text`/`bot_text` — konversationer syns tomma.** |
| Enhetstester | `tests/test_core.py`, `tests/test_consent.py` | 12 tester, ingen API-nyckel. |
| Persona-matris | `scripts/run_tests.py` | 6 personor mot live Gemini (Ella, Omar, Saga, Leo, Nour, Ville). README: 46/47. |
| Eval | `scripts/gemini_eval.py` | 3 sokratiska fall. |

### Vad som faktiskt funkar
- Föräldersamtycke innan chatt.
- Sessionsgräns 30 meddelanden / 15 min paus / 100 per dygn (i minnet).
- Sokratisk linje i prompt + tester mot "ge mig svaret".
- Krisregel med BRIS i prompt + Leo-persona.
- Anti-jailbreak i prompt + Saga-persona.
- Röstmeddelanden avvisas.
- Ett dokumenterat barntest (9-åring, klocka).
- AGPL-3.0, opensverige, README på svenska.

### Hål i Yta B
- `ALLOWED_CHAT_ID = 544123218` hårdkodat — inte opensourcebart.
- Prompten duplicerar och *motsäger* `agents/tutor/*` (AI-identitet).
- Policies (`max_minutes_*`, klockslag) läses in men används inte.
- Ingen input-safety i kod före Gemini.
- Ingen bildinläsning trots feltexter och roadmap v0.3.
- Historik dör vid process-omstart.
- Ett barn / en profil. Inget stödläge-val för föräldern.
- Dashboard visar inte loggtext (fältbug).
- Gemini Paid Tier 1 = data lämnar hemmet. Strider mot lokal-först.

## Yta A — FastAPI + Ollama (det AGENTS.md beskrev)

| Del | Fil | Status |
|-----|-----|--------|
| API | `backend/main.py` | `/api/chat`, `/api/health`, `/api/reports`. Ingen auth. |
| Pipeline | `backend/pipeline.py` | preflight → safety_in → RAG → LLM → safety_out → logg + HMAC-audit. |
| Safety | `backend/safety.py` | Bara engelska regex. Inget svenskt, ingen krisdetektion. |
| RAG | `backend/rag.py` | Chroma + Ollama-embeddings. Tom `vault/curriculum-vectors/`. |
| Session | `backend/session_store.py` | SQLite, 40 meddelanden. |
| Reports | `backend/reports.py` | Läser `vault/parent-reports/*.json` — mappen är tom. |
| Chat-UI | `frontend/index.html` | Enkel HTML-chat, länk till föräldravy. |
| Föräldravy | `frontend/guardian.html` | Listar statiska rapporter, ingen auth, ingen live-logg. |
| Docker | `Dockerfile`, `docker-compose.yml` | Port 8080, mountar vault/agents/frontend. |

### Vad som faktiskt funkar
- En enda pipeline-sanning för lokal körning.
- Prompt byggd från SOUL + SKILL + RULES + profil (rätt mönster).
- Kedjad, HMAC-signerad audit.
- RAG-arkitektur redo när Lgr22-filer finns.
- Noll molnplikt.

### Hål i Yta A
- Ingen samtyckesgate.
- Ingen förälder-auth på chatt eller reports.
- Safety för svag för barn.
- Ingen Lgr22 i vault (sample ignoreras av gitignore-mönster).
- Ingen testhärd för pipeline/safety/RAG.
- UI är scaffold, inte barnvänligt.
- Två config-träd (`config/` vs `vault/config/`) med samma JSON.

## Data och kursplan

| Resurs | Innehåll | Lucka |
|--------|----------|-------|
| `config/lgr22/ak4.json` | 10 poster: matte 5, svenska 3, NO 2 | Bara åk 4. Inget SO, engelska, idrott, bild, musik. |
| `config/lgr22/grundposter.json` | 3 förmågor | Bra frö, inte kopplat till undervisningssteg. |
| `config/child_profile.json` | Test-Elev, dinosaurier + Minecraft | Inga stödpreferenser (tillagt i den här branchen). |
| `config/policies.json` | tid, safety, sokratisk | Ingen `parent_controls` före den här branchen. |
| `vault/curriculum-vectors/` | gitkeep | RAG har inget att äta. |
| `vault/parent-reports/` | gitkeep | Guardian-HTML är tom. |
| `scripts/curriculum_cli.py` | list + validate | Ingen import från Skolverket, ingen åk 5–6. |

## OSS- och driftläge

| Finns | Saknas |
|-------|--------|
| LICENSE AGPL-3.0 | CI (pytest + research validate + curriculum validate) |
| README + roadmap | Issue/PR-mallar (den här branchen lägger CONTRIBUTING + SECURITY) |
| `.env.example` | CODE_OF_CONDUCT, secret scanning, Dependabot |
| 12 enhetstester | `pytest` fanns inte i `requirements.txt` |
| Docker för Yta A | Image/tag-strategi, SBOM, "run offline"-guide som stämmer |

## Testad kvalitet
- Enhetstester: 12/12 (profil + consent), inget för bot-gränser,
  logger, dashboard, safety, pipeline.
- Persona-matris: stark på Sokratik, jailbreak, BRIS — men kräver
  betald Gemini och är inte CI.
- Ett barntest. Ingen uppföljning, ingen NPF-persona, ingen
  flerspråkig utöver Nour.

## Slutsats
Vi har **pedagogisk ryggrad i text** och **två halva produkter**.
För att opensourca något vi är stolta över måste kärnan bli en,
föräldern måste kunna styra på riktigt, extra stöd måste sitta i
kod och kursplan, och research måste mata backlogen — inte bara
en README-lista.
