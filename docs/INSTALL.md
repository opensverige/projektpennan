# Installera — webben först, sen den väg ni vill

Kontaktnamn: Gnista. Vi ger **basplattan**. Ni formar den och
jackar in den modell ni vill. Monument: [docs/BASEPLATE.md](BASEPLATE.md).

Onboarding **börjar på webben**. Inte Docker. Inte `/consent`.
Öppna `frontend/start.html` (eller http://localhost:8080/start.html
när stacken kör). Den spottar ur `runtime.json` + `.env`.

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

Från start-sidan: välj ChatGPT / Claude / Gemini / egen endpoint.
Ladda ner `.env`. Lägg den i projektroten. **Skicka inte nyckeln
till oss.** Ni betalar leverantören. Ni godkänner att läxtext
lämnar hemmet.

```
OPENAI_API_KEY=sk-...          # eller ANTHROPIC_ / GEMINI_
# runtime.json: provider + model + base_url
```

Tills P-26 är klar gör nyckeln *ingenting* i FastAPI-chatten.
Telegram-boten läser fortfarande bara `GEMINI_API_KEY`.
Receptet är sant. Kopplingen är nästa PR.

## D. Telegram som den ser ut nu

```bash
pip install -r requirements.txt
cp .env.example .env
python -m skooli_buddy.bot
```

`/consent [lösenord]` → `/start`. Hårdkodat chat-id (P-02).
Det är inte räkmackan och inte webbstarten.

---

## Vad som medvetet inte krävs

- BankID för att *börja* (Hem kan lägga det sen)
- Att föräldern kan Docker (väg C + sen Hem)
- Barnkonto, QR, “nu prata med AI:n”
- Att *vi* äger modellvalet
