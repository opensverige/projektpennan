# Skooli Buddy

> En sidekick för barn som behöver stöd i skolan. Föräldern sitter i
> spakarna. Skolans system gör det inte. Ger aldrig svaret.
> Arbetsnamn. Kernel föräldern äger — egna agenter, egen världsbild.

**Projekt Pennan** är ett open-source-initiativ under
[opensverige](https://github.com/opensverige) / [opensverige.se](https://opensverige.se).
Skooli Buddy är den första produkten. Licens: AGPL-3.0.

---

## Vad är det?

Barnet (9–12 år, åk 4–6 först) chattar med en studiekompis som leder
med frågor, små steg, saga, lek och extra stöd — inte facit. Inte
läx-nudge. Lgr22 är ett *valfritt pack*, inte överhet. Föräldern ger
samtycke, kan pausa, radera, byta världsbild och ladda egna agenter.
Ingen lärarvy. Ingen klasslista. Ingen Unikum-export.

Plattformen: [docs/PLATFORM.md](docs/PLATFORM.md).

```
Barn: "Vad är 7 gånger 8?"
Skooli: "Vet du vad 7 gånger 7 är? Då kan vi räkna ett steg till! 🤔"
```

Läs [docs/PRODUCT.md](docs/PRODUCT.md) för visionen,
[docs/PRODUCTIZATION.md](docs/PRODUCTIZATION.md) för open-core
(kernel / Hem / egen drift),
[docs/INVENTORY.md](docs/INVENTORY.md) för vad som faktiskt är byggt
och [docs/BACKLOG.md](docs/BACKLOG.md) för vad som återstår.

Barnet möter oss som en kontakt i chatten de redan har (WhatsApp
i Sverige), inte som en QR eller en ny app. Telegram är Open-yta.

---

## Två ytor (samma mål)

| | Hem / lokal (default för OSS) | Messaging (det som testats mot barn) |
|---|-------------------------------|--------------------------------------|
| Kod | `backend/` + `frontend/` + `vault/` | `skooli_buddy/` + `dashboard/` |
| Modell | Ollama på din maskin | Gemini 2.5 Flash (opt-in) |
| UI | HTML-chat på localhost:8080 | Telegram + Streamlit |
| Status | Scaffold med RAG + audit | Live-testad, 12 enhetstester |

Målet är **en kärna, två ytor**. Just nu är de parallella. Se P-01.

---

## Stack

| Del | Teknologi |
|-----|-----------|
| Lokal server | FastAPI + Ollama + Chroma |
| Bot | Python + python-telegram-bot v21+ |
| Valfri moln-LLM | Google Gemini 2.5 Flash |
| Föräldrapanel | Streamlit (Telegram) / `guardian.html` (lokal) |
| Loggning | JSONL + HMAC-audit i vault |
| Kursplan | Valfritt pack. Lgr22 i `config/lgr22/` + `vault/packs/lgr22/` |

---

## Quickstart

```bash
# 1. Klona och installera
git clone https://github.com/opensverige/projektpennan
cd projektpennan
pip install -r requirements.txt

# 2. Konfigurera
cp .env.example .env
# Fyll i TELEGRAM_BOT_TOKEN, GEMINI_API_KEY, GUARDIAN_PASSPHRASE

# 3. Starta boten
python -m skooli_buddy.bot
```

Telegram-boten har just nu ett hårdkodat tillåtet chat-id (P-02).
Sätt inte den i produktion åt andra familjer innan det är env-styrt.

### Lokal stack (ingen moln-LLM)

```bash
# Kräver Ollama med t.ex. hermes3:8b på port 11434
docker compose up --build
# http://localhost:8080
```

Backend-only: `pip install -r backend/requirements.txt` och
`uvicorn main:app --reload --host 0.0.0.0 --port 8080` från `backend/`.

### Föräldrapanel

```bash
streamlit run dashboard/app.py
```

Logga in med `GUARDIAN_PASSPHRASE`. Panelen visar antal meddelanden, aktiva dagar och de senaste 50 konversationsturerna (anonymiserade).

### Curriculum CLI

```bash
python scripts/curriculum_cli.py list      # Lista alla Lgr22-poster
python scripts/curriculum_cli.py validate  # Validera JSON-format
```

Lägg till fler Lgr22-data som `.json`-filer i `config/lgr22/` — samma schema som befintliga filer.

---

## Föräldrainstruktioner

Barn under 13 år faller under digital samtyckesålder i Sverige. **Samtycke måste ges innan barnet kan chatta.**

1. Öppna boten i Telegram
2. Skriv: `/consent [ditt-lösenord]`
3. Bekräfta att du tagit del av integritetsinformationen
4. Ditt barn kan nu skriva `/start` och börja

Återkalla samtycke och radera all data: `/revoke`

---

## Säkerhet

Skooli Buddy har **13 absoluta regler** hårdkodade i systempromptena — skrivna av människor, inte genererade av AI:

- Svarar alltid på svenska
- Ger **aldrig** ett rakt svar på en skoluppgift
- Max 2 korta meningar + 1 fråga per svar
- Anti-jailbreak: byter aldrig personlighet oavsett prompt
- Samlar aldrig in personuppgifter
- Hänvisar till **BRIS 116 111** vid allvarliga signaler
- Blockerar ämnen som inte hör hemma i ett klassrum

Barn kan inte kringgå reglerna. Reglerna kan inte kringgå boten.

---

## Status

| Test | Resultat |
|------|----------|
| Enhetstester | 12/12 gröna |
| Persona-tester (Sokratisk metod) | 46/47 PASS |
| Första riktiga barntest (9-åring) | ✅ Framgångsrik klocka-konversation |

---

## Roadmap

Levande lista: [docs/BACKLOG.md](docs/BACKLOG.md).
Research som styr den: `python scripts/research_pipeline.py summary`.

Kort:

- **P0** — en kärna, inget hårdkodat chat-id, safety i kod, CI, ärlig README, fungerande föräldrainlogg + `/pause`
- **P1** — föräldern styr stödläge/tid/export, Lgr22-pack åk 4–6, läx-foto opt-in, lokal modell som default, minne hemma
- **P2** — röst, fler årskurser, WhatsApp, veckosammanfattning utan betyg
- **P3** — kernel/Hem/BYO, WhatsApp-kontakt hos barnet, förälder-PWA, DPIA innan sälj
- **P4** — pack-laddare, världsbild, fler metoder i kod, krypterade anpassningar

Spectator-grupp, bildstöd och minne från den gamla v0.2–v0.4-listan
ligger kvar som P-13, P-12, P-10. Produktmodellen:
[docs/PRODUCTIZATION.md](docs/PRODUCTIZATION.md).

---

## GDPR

- **Dataminimering:** Bara numeriskt `chat_id` sparas — aldrig namn eller personuppgifter
- **Samtycke:** Förälders samtycke krävs (GDPR Art. 8, barn under 13 år)
- **Rätt till radering:** `/revoke` raderar all data omedelbart
- **Datalagring:** Bara lokalt på din server, aldrig delat med tredje part
- **Gemini Paid Tier 1:** Google använder inte datan för modellträning

---

## Varför Skooli Buddy?

Ingen öppen produkt kombinerar:
- Svenska + valfri kursplan (Lgr22 som pack)
- Flera metoder **och** extra stöd (Sokrates, worked, CPA, saga, lek)
- Föräldern som operatör — världsbild, egna agenter, inte skolan
- Messaging *eller* helt lokalt. Ingen vendor lock-in.
- AGPL, research-pipeline, regler i git

Khanmigo är närmast pedagogiskt, men är skol-/US-spåret.
Sorin/Tutur/Latio har föräldrakontroll, men är stängda och engelska.

## Research

```bash
python scripts/research_pipeline.py validate
python scripts/research_pipeline.py summary
python scripts/research_pipeline.py backlog
```

Nytt påstående: se [research/README.md](research/README.md).
Fynd utan källa får inte styra backlogen.

---

## Bidra

Läs [CONTRIBUTING.md](CONTRIBUTING.md). Kort:

```bash
git checkout -b feat/din-feature
python -m pytest tests/ -v
python scripts/research_pipeline.py validate
# Öppna en PR mot main
```

Säkerhetsfel: [SECURITY.md](SECURITY.md), inte ett publikt issue.

Frågor? [github.com/opensverige/projektpennan](https://github.com/opensverige/projektpennan)
eller [opensverige.se](https://opensverige.se).

---

## Tester

```bash
python -m pytest tests/ -v
```

---

*Projekt Pennan — AI för svensk utbildning, byggt öppet.*
