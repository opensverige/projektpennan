# Installera — vad som finns, vad som är monumentet

Arbetsnamn: Skooli Buddy. Kernel föräldern äger.

Det finns **två installationer**. Blanda inte ihop dem.

| | **Idag (byggt)** | **Hem (monumentet, ej byggt)** |
|---|------------------|--------------------------------|
| Vem | Tech-förälder, bidrag, vi som utvecklar | Vanlig familj, fem minuter |
| Barn ser | Telegram-bot eller localhost:8080 | En tyst kontakt i WhatsApp |
| Förälder gör | Klona, `.env`, `/consent [lösen]` | BankID på *sin* telefon, barnet inte i rummet |
| Onboarding | Nej. Kommandon. | Ja — P-28. Inte byggt. |
| Barn-onboarding | Avsiktligt ingen | Avsiktligt ingen |

---

## Scenariot vi håller uppe (Hem)

Söndag kväll. Barnen är i sitt rum.

1. Föräldern öppnar Hem på sin telefon. BankID. Inte barnets skärm.
2. Kort samtycke. Inklusive: chatten kan gå via WhatsApp/Meta.
3. Barnkort: tilltalsnamn, åk, stöd. Valfritt: världsbild, diagnos,
   veckans skolteman. Aldrig krav.
4. Tid: 45 min, stopp 19:30. Inget läxlarm.
5. Samma gest som att lägga till mormor: en kontakt i barnets WhatsApp.
6. PIN på föräldrapanelen. Pausa / radera där.
7. Klart. Ingen demo med barnet i knät.

Barnet ser aldrig BankID, aldrig pris, aldrig loggen.
Första gången de skriver i tråden är första gången produkten börjar.

Det är `docs/UX-SCENARIOS.md` och `docs/PRODUCTIZATION.md`.
Koden för det är backlog **P-28** (plus P-27, P-30, P-32).
**Den onboarding-flödet är inte byggt.**

---

## Scenariot som går att köra i kväll (Open)

### A. Lokal kernel — ingen moln-LLM

Föräldern (eller du) har Docker och Ollama.

```bash
git clone https://github.com/opensverige/projektpennan
cd projektpennan
# Ollama med t.ex. hermes3:8b på port 11434
docker compose up --build
```

Öppna http://localhost:8080 — det är HTML-chatten.
`frontend/guardian.html` är en tunn föräldralogg, inte Hem-panelen.
Ingen BankID. Ingen WhatsApp-kontakt. Ingen fem-minuters-guide.

Vaulten ligger i `vault/`. Packs (världsbild, Lgr22, skolkontext,
egen agent) är mallar i `vault/packs/`. Laddaren är P-33 — du
redigerar filer för hand.

### B. Telegram — det som testats mot ett barn

```bash
pip install -r requirements.txt
cp .env.example .env
# TELEGRAM_BOT_TOKEN, GEMINI_API_KEY, GUARDIAN_PASSPHRASE
python -m skooli_buddy.bot
```

Sedan, i Telegram:

1. Föräldern skriver `/consent [lösenord]`
2. Barnet (eller samma chatt) skriver `/start`
3. Föräldrapanel: `streamlit run dashboard/app.py`

Det är **inte** en onboarding. Det är kommandon. Boten har dessutom
ett hårdkodat tillåtet chat-id (P-02) — den är inte redo att delas
ut till andra familjer.

`/pause` lovas i samtyckestexten men saknas (P-07).

---

## Vad som medvetet inte finns

- Ingen wizard. Ingen QR. Ingen “nu ska du prata med AI:n”.
- Ingen barn-onboarding (avatar, “vad vill du lära dig”).
- Ingen BankID, ingen start-länk, ingen WhatsApp-adapter.
- Ingen pack-UI — vaulten är filer, som Obsidian.

När Hem byggs ska den här filen fortfarande vara sann:
Open = klona och kör. Hem = BankID och en tyst kontakt.
Samma kernel. Samma safety. Olika hur den hamnar hos barnet.
