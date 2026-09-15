# Installera — webben först, sen den väg ni vill

Kontaktnamn: Gnista. Vi ger **basplattan**. Ni formar den och
jackar in den modell ni vill. Monument: [docs/BASEPLATE.md](BASEPLATE.md).

Onboarding **börjar på webben**, en skärm.
Öppna `frontend/start.html`. Namn, ev. nyckel, sätt igång.
UI-källan är `web/` (shadcn). Efter ändring: `cd web && npm run build`.
Inte Docker-först. Inte `/consent`. Inte sex steg.
Av-ramp för päron bakom “Bygger du själv?”.

Barnet har ingen onboarding.

---

## Välj väg efter starten

| Väg | Kommando / gest | Modell i kväll | Ärligt läge |
|-----|-----------------|----------------|-------------|
| A. Webb + Docker + Ollama | `docker compose up --build` | lokal | **Byggt** |
| B. Docker + egen nyckel | samma + `.env` från starten | ChatGPT / Claude / Gemini | Recept klart. Adapter = P-26 |
| C. Bara filer | start.html → ladda ner config | — | Plattan, ingen chatt än |
| D. Telegram | `python -m skooli_buddy.bot` | Gemini, hårdkodat | Byggt som kommandon |
| E. Hem | BankID, tyst kontakt | vi eller BYO | Inte byggt |
| F. WhatsApp | kontakt i listan | samma kernel | P-32 |

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
låsa modell. Laddaren är P-26. Tills dess läser backend
`OLLAMA_URL` + `MODEL_NAME`.

## B. Samma platta, er frontier-modell

Från start-sidan: klistra in nyckeln. Prefixet väljer
ChatGPT / Claude / Gemini / Grok tyst. **Skicka inte nyckeln
till oss.** Ni betalar leverantören. Ni godkänner att läxtext
lämnar hemmet.

```
OPENAI_API_KEY=sk-...          # eller ANTHROPIC_ / GEMINI_
# runtime.json: provider + model + base_url
```

Tills P-26 är klar gör nyckeln *ingenting* i FastAPI-chatten.
Telegram-boten läser fortfarande bara `GEMINI_API_KEY`.
Receptet är sant. Kopplingen är nästa PR.

## D. Telegram — deras bot, vår start-länk

Ingen officiell @gnista-bot. Ingen verifier-bot som tar emot token
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

## Vad som medvetet inte krävs

- BankID för att *börja* (Hem kan lägga det sen)
- Att föräldern kan Docker (väg C + sen Hem)
- Barnkonto, QR, “nu prata med AI:n”
- Att *vi* äger modellvalet
