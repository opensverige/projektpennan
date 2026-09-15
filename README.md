# Gnista

[Svenska](README.md) · [English](README.en.md) · [Español](README.es.md) · [العربية](README.ar.md)

**En studiekompis för åk 4–6. Föräldern äger plattan. Barnet får frågor, inte facit.**

Kontaktnamnet — det barnet skriver till — är **Gnista**.  
Repot och initiativet heter **Projekt Pennan**, under [Open Sverige](https://opensverige.se).  
Licens: [AGPL-3.0](LICENSE).

`Skooli Buddy` och `Stjärnis` är inte produktnamn. Det första krockar med Homework Buddy / Studybuddy. Det andra låser in oss hos niorna och stöter bort tolvåringar.

---

## Vad det är

När läxan kärvar ska barnet kunna fråga en kompis som:

1. aldrig ger svaret först,
2. anpassar tempot,
3. tål “jag är dum” utan att hålla med,
4. stannar när det blir jobbigt,
5. syns för föräldern.

```
Barn:   Vad är 7 gånger 8?
Gnista: Vet du vad 7 × 7 är? Då tar vi ett steg till.
```

Vi ger **basplattan**: safety, samtycke, vault, pack-format, logg.  
Föräldern formar den och jackar in den modell de vill — Ollama hemma, eller ChatGPT / Grok / en egen nyckel. Plattan består när hjärnan byts.

Lgr22 är ett *valfritt pack*, inte överhet. Världsbild, tro och egna agenter är förälderns. Extra stöd är default. Inget läxgnäll.

Vi bygger **inte** för rektorer, kommuner, Unikum eller klasslistor. Skolan får rekommendera oss. De får inte drifta oss.

---

## Vad det inte är

| Inte | Utan |
|------|------|
| En facit-app | Frågor, små steg, saga, lek |
| Skolans system | Ett hemverktyg |
| En låst lärare | En kernel + packs föräldern byter |
| En barn-app med QR | En kontakt i en chatt de redan har |
| Prompt-regler | Regler i kod. Barnet kan inte stänga av dem. |

---

## Testa i kväll

Onboarding börjar på webben när den ytan är på plats. Det som **finns på `main` i kväll** är Open: lokal chatt eller Telegram.

### 1. Lokal platta (default)

Ingen moln-LLM. Data stannar i `vault/`.

```bash
git clone https://github.com/opensverige/projektpennan
cd projektpennan
# Ollama med t.ex. hermes3:8b på 11434
docker compose up --build
```

[http://localhost:8080](http://localhost:8080) — barnchatt.  
[http://localhost:8080/guardian.html](http://localhost:8080/guardian.html) — tunn logg.

Utan Docker: `pip install -r backend/requirements.txt` och `uvicorn main:app --reload --host 0.0.0.0 --port 8080` från `backend/`.

### 2. Telegram (valfritt, egen bot)

Ingen officiell `@gnista`. Föräldern skapar boten hos [@BotFather](https://t.me/BotFather). Tokenen stannar hos dem. Om *vi* tar emot tokenen ser vi chatten i klartext — det gör vi inte.

```bash
pip install -r requirements.txt
cp .env.example .env   # TELEGRAM_BOT_TOKEN, ev. GEMINI_API_KEY
python -m skooli_buddy.bot
```

På `main` finns fortfarande ett hårdkodat tillåtet chat-id (P-02). Kör inte den boten åt andra familjer förrän allowlist + start-länk är inne.

Hem — BankID, tyst WhatsApp-kontakt, fem minuter — är monumentet. **Inte byggt.** Se [docs/INSTALL.md](docs/INSTALL.md).

---

## Plattan

```
  packs / egen agent / världsbild     ← föräldern skriver
              │
  modell (BYO)                        ← de jackar in, de byter
              │
  yta: webb · Docker · Telegram · WA  ← de väljer hur den lever
              │
  ┌───────────┴────────────┐
  │  SAFETY  samtycke  logg │  ← vi. går inte att stänga av
  │  pack-format  vault     │
  └─────────────────────────┘
```

**Open:** de hostar. Vi ser inte deras chatter.  
**Hem:** vi hostar. Då ser vi dem, Telegram/WhatsApp ser dem, och vi behöver DPIA innan första familjen betalar. Safety får aldrig bli paywall.

Hur man sätter upp och byter väg: [docs/INSTALL.md](docs/INSTALL.md).  
Vad som är kernel vs pack: [docs/PLATFORM.md](docs/PLATFORM.md).  
Open / Hem / egen drift: [docs/PRODUCTIZATION.md](docs/PRODUCTIZATION.md).

---

## Säkerhet och integritet

Koden validerar. Modellen undervisar.

- Kris → människa. **BRIS 116 111.** Ingen chatbot-terapi, ingen följdfråga.
- Sex, våld, droger → en vuxen hemma, inte modellen.
- Inga hemligheter från föräldern.
- Jailbreak byter inte personligheten. Reglerna sitter inte i prompten.
- Numeriskt id, inte namn eller skol-id. `/revoke` raderar.
- Diagnos bara om *föräldern* skrivit den. Tomt = extra-stöd-default.

Spec: [SKOOLI_BUDDY_SAFETY_SPEC.md](SKOOLI_BUDDY_SAFETY_SPEC.md).  
Tutorregler: `agents/tutor/SOUL.md` + `SKILL.md` + `RULES.md`.

Samtycke krävs innan barnet chattar (GDPR art. 8, under 13). På Telegram-ytan i dag: `/consent`, återkalla med `/revoke`.

---

## Ärligt läge

Två halva produkter, samma mål. **En kärna är P-01.**

| | Lokal stack | Messaging-stack |
|---|-------------|-----------------|
| Kod | `backend/` · `frontend/` · `vault/` | `skooli_buddy/` · `dashboard/` |
| Modell i kväll | Ollama | Gemini (opt-in) |
| UI | HTML på `:8080` | Telegram + Streamlit |
| Status | RAG + HMAC-audit, tunn chatt | Live-testad mot barn, 12 tester |

Frontier-nyckel i onboarding (ChatGPT / Claude / Grok) är receptet. **Adapter = P-26 — inte kopplad än.** Att klistra en nyckel gör ingenting i FastAPI-chatten i kväll.

Vad som faktiskt är byggt: [docs/INVENTORY.md](docs/INVENTORY.md).  
Vad som återstår: [docs/BACKLOG.md](docs/BACKLOG.md).  
Vision: [docs/PRODUCT.md](docs/PRODUCT.md).

---

## Repo

| Sök här | För det här |
|---------|-------------|
| `agents/tutor/` | Persona och pedagogik |
| `backend/` | FastAPI, pipeline, safety, vault |
| `frontend/` | Lokal chatt + föräldravy |
| `vault/` | Barnkort, policies, logg, packs — strukturen rörs inte |
| `skooli_buddy/` | Telegram-yta |
| `config/lgr22/` | Kursplansposter som pack |
| `research/` | Fynd. Utan källa får de inte styra backlogen |
| `docs/` | Produkt, platta, install, inventory |

Testprofilen “Test-Elev” får ligga kvar. Riktiga barnprofiler committas aldrig.

---

## Språk i det här repot

`README.md` är sanningen. Den är svenska — produkten är svensk skola,
svensk förälder, svensk BRIS.

Korta översättningar ligger bredvid: `README.en.md`, `README.es.md`,
`README.ar.md`. Samma mönster som Vue och Rust. Inte fyra kompletta
manualer. Inte i18n i koden. Barnet pratar fortfarande svenska.
Packs kan senare bära ett annat undervisningsspråk. Det är inte det här.

När du ändrar vad produkten *är* eller hur man startar den: börja i
svenska README, sen de korta. Kommandon (`git`, `docker`) översätts inte.

---

## Bidra

Läs [CONTRIBUTING.md](CONTRIBUTING.md) innan du kodar. Kort:

```bash
git checkout -b feat/kort-beskrivning
python -m pytest tests/ -v
python scripts/research_pipeline.py validate
python scripts/curriculum_cli.py validate
```

Nytt påstående om pedagogik eller safety: `python scripts/research_pipeline.py new` — se [research/README.md](research/README.md).

Vi mergar inte: skola som operatör, diagnosstämpel, prompt-only safety, hemliga chat-id eller riktiga barn i git.

Säkerhetsfel: [SECURITY.md](SECURITY.md), inte ett publikt issue.

---

*Projekt Pennan — öppen kernel för läxhjälp hemma. Inte en skolapp.*
