# Installera — webben först, sen den väg ni vill

Kontaktnamn: Utter. Vi ger **basplattan**. Ni formar den och
jackar in den modell ni vill. Monument: [docs/BASEPLATE.md](BASEPLATE.md).

Onboarding **börjar på webben**, en skärm.
Skiss av hemsidan: `frontend/land.html` (drawably, tre sektioner).
Öppna `frontend/start.html`. Namn, ev. nyckel, sätt igång.
UI-källan är `web/` (shadcn). Efter ändring: `cd web && npm run build`.
Inte Docker-först. Inte `/consent`. Inte sex steg.
Av-ramp för päron bakom “Bygger du själv?”.

Barnet har ingen onboarding.

---

## Välj väg efter starten

| Väg | Kommando / gest | Modell i kväll | Ärligt läge |
|-----|-----------------|----------------|-------------|
| A. Webb + Docker + Ollama | `UTTER_USE_OLLAMA=1 docker compose up --build` | lokal, sista utväg | Byggt, inte default |
| B. Webb + egen modell | nyckel i starten eller env | ChatGPT / Grok / Claude / Groq / vLLM | **Byggt (P-26)** |
| C. Bara filer | start.html → ladda ner config | — | Plattan, ingen chatt än |
| D. Telegram | `python -m skooli_buddy.bot` | Gemini, hårdkodat | Byggt som kommandon |
| E. Hem | BankID, tyst kontakt | vi eller BYO | Inte byggt |
| F. WhatsApp | kontakt i listan | samma kernel | P-32 |
| G. Testa nu | `./scripts/demo.sh` | kärna, inte Grok | **Byggt** |
| H. Testa SOUL | `./scripts/soul.sh` | samma BYO-modell + tutorfiler | **Byggt** |

Byt väg senare. Samma vault. Samma barnkort.

---

## A. Lokal platta, data hemma

```bash
git clone https://github.com/opensverige/projektpennan
cd projektpennan
# Ollama med t.ex. hermes3:8b på 11434
docker compose up --build
```

http://localhost:8080 — barnchatt.  
http://localhost:8080/start.html — förälderstart.  
http://localhost:8080/guardian.html — tunn logg.

`vault/config/runtime.example.json` → `runtime.json` när ni vill
låsa modell. Backend läser den, sen env (`OPENAI_API_KEY`,
`XAI_API_KEY`, `ANTHROPIC_API_KEY`, `GROQ_API_KEY`,
`OPENAI_BASE_URL`). Ollama bara om ni valt `provider: ollama`.

## B. Samma platta, er frontier-modell

Från start-sidan: klistra in nyckeln. Prefixet väljer
ChatGPT / Claude / Gemini / Grok tyst. **Skicka inte nyckeln
till oss.** Ni betalar leverantören. Ni godkänner att läxtext
lämnar hemmet.

```
OPENAI_API_KEY=sk-...          # eller ANTHROPIC_ / GEMINI_
# runtime.json: provider + model + base_url
```

Nyckeln i starten skickas bara till er lokala `/api/chat`
(header, loggas inte). Telegram-boten läser fortfarande
`GEMINI_API_KEY` tills P-01 slår ihop ytorna.

## D. Telegram — deras bot, vår start-länk

Ingen officiell @utter-bot. Ingen verifier-bot som tar emot token
(då sitter *vi* på nyckeln). Bara @BotFather kan skapa en bot.

1. På `test.html`: Öppna @BotFather → `/newbot` → klistra token.
2. Vi kör `getMe` *här*. Får en länk `t.me/DinBot?start=…`.
3. Föräldern öppnar länken. Den chatten släpps in. Andra ignoreras.
4. `python -m skooli_buddy.bot` hos dem (eller Docker). Tom allowlist
   utan start-länk = vägrar starta. Inget hårdkodat chat-id.

```bash
pip install -r requirements.txt
cp .env.example .env
python -m skooli_buddy.bot
```

---

## G. Testa chatten nu (kärna, inte Grok)

Ingen Ollama. Ingen nyckel. Samma safety som barnet får.

```bash
pip install fastapi uvicorn pydantic httpx
./scripts/demo.sh
```

http://127.0.0.1:8080/start.html — namn, samtycke.  
http://127.0.0.1:8080/test.html — chips, även opassande.  
http://127.0.0.1:8080/index.html — skriv som barnet.

Läxfrågor får ett sokratiskt stubbsvar. Sex / bomb / hemlighet /
kris / jailbreak kommer från `safety.py`, inte från en modell.
P-26 är kopplad: samma safety före och efter, oavsett modell.

## H. Testa SOUL (riktig agent, inte stubbar)

Samma `SOUL.md` + `SKILL.md` + `RULES.md` som pipelinen staplar.
Läxa går till den modell ni jackat in. Kris/sex/hemlighet stannar i `safety.py`. Svaret filtreras också.

```bash
export OPENAI_API_KEY=sk-...   # eller GROQ_ / XAI_ / ANTHROPIC_
./scripts/soul.sh
```

http://127.0.0.1:8080/index.html — skriv som barnet.

Chips på `test.html` är fortfarande kärnan (förälderns plan).
Chatten är SOUL. Inte samma sak.

---

## Vad som medvetet inte krävs

- BankID för att *börja* (Hem kan lägga det sen)
- Att föräldern kan Docker (väg C + sen Hem)
- Barnkonto, QR, “nu prata med AI:n”
- Att *vi* äger modellvalet
