# Basplattan — vi ger golvet, de formar huset

Kontaktnamn: Gnista. Initiativ: Projekt Pennan.

> Vi säljer inte en färdig lärare. Vi säljer **plattan**:
> safety, samtycke, pack-format, logg, ytor.
> Föräldern jackar in ChatGPT, Claude, Gemini, Ollama
> eller en egen OpenAI-kompatibel endpoint. De byter
> när en bättre modell kommer. Plattan består.

Homework Buddy och Allakando *är* läraren. En modell, en app,
deras pedagogik. Det är inte frihet. Det är en produkt.

## Vad som är plattan

```
     packs / egen agent / världsbild     ← föräldern skriver
                 │
     modell (BYO)                        ← de jackar in, de byter
                 │
     yta: webb · Docker · Telegram · WA  ← de väljer hur den lever
                 │
  ┌──────────────┴──────────────┐
  │  SAFETY  samtycke  logg     │  ← vi. går inte att stänga av
  │  pack-format  vault         │
  └─────────────────────────────┘
```

**Vi lovar inte den smartaste modellen.** Vi lovar att en ny
frontier-modell kan skruvas i utan att byta barn, pack eller
chattlista. Det är så den *utvecklas*: plattan är stabil,
hjärnan byts.

## Onboarding börjar på webben

Inte Docker först. Inte `/consent [lösen]`. Inte BankID-default.

1. Föräldern öppnar **webben** (den här datorn eller Hem sen).
2. Kryssar: jag är vårdnadshavare.
3. Formar: extra stöd / saga / tro / tre rader egen.
4. Barnkort: tilltalsnamn + åk.
5. Jackar in en modell *eller* säger “lokalt, ingen nyckel”.
6. Väljer hur den ska leva: i webbläsaren, Docker, Telegram.
7. Får ett recept: `runtime.json` + `.env`. Inget barn i knät.

Barnet har ingen onboarding. Första gången de skriver är
första gången produkten börjar.

Klickbar start: `frontend/start.html`. Monumentet är den här
filen. Live ChatGPT-anrop är P-26 — start-sidan ljuger inte.

## Flera sätt att installera (samma platta)

| Väg | Vem | Modell | Barn ser | Byggt? |
|-----|-----|--------|----------|--------|
| **Webb nu** | Förälder på localhost | Ollama om den kör | `index.html` | Delvis (ingen adapter) |
| **Docker + Ollama** | Tech-förälder | lokal, data hemma | localhost:8080 | Ja, kvällens Open |
| **Docker + egen nyckel** | Tech som vill GPT/Claude | deras konto, deras ToS | samma chatt | Recept. Kod = P-26 |
| **Telegram** | Den som redan har bot | idag Gemini hårdkodat | 1:1-bot | Ja, kommandon. Inte räkmacka |
| **Hem** | Vanlig familj | vi betalar EU, eller BYO | tyst kontakt | Monument. Inte byggt |
| **WhatsApp** | Svensk default sen | samma kernel | kontakt i listan | P-32 |

Alla vägar läser samma vault och samma safety. Byter de från
Ollama till ChatGPT byter de *en fil*, inte barnet.

## Jacka in en modell

`vault/config/runtime.json` (exempel i `runtime.example.json`):

```json
{
  "provider": "openai-compat",
  "base_url": "https://api.openai.com/v1",
  "model": "gpt-4.1",
  "api_key_env": "OPENAI_API_KEY"
}
```

Samma form för Claude, Gemini, en proxy, en lokal LM Studio.
Nyckeln ligger i miljön hos *dem*. Start-sidan sparar den inte
hos oss. BYO = de kryssar: datan går till *min* leverantör.

Safety körs **före och efter** anropet. En starkare modell får
inte ge facit först. Plattan vinner mot modellen.

## Vad vi medvetet inte är

- En ChatGPT-wrapper med uggla
- En låst Allakando-pedagogik
- En skola-som-operatör
- “Bästa modellen 2026” som säljargument
