# Skooli Buddy

En personlig AI-studiekompis för svenska barn i åk 4–6, driven av Gemini 2.5 Flash och Sokratisk pedagogik — den ger aldrig raka svar.

## Quickstart

```bash
# 1. Klona och installera
git clone https://github.com/Baltsar/projektpennan
cd projektpennan
pip install -r requirements.txt

# 2. Konfigurera miljövariabler
cp .env.example .env
# Redigera .env med dina nycklar

# 3. Skaffa Telegram Bot Token
# Prata med @BotFather på Telegram, skapa en ny bot

# 4. Starta boten
python -m skooli_buddy.bot
```

## Konfiguration (.env)

| Variabel | Beskrivning |
|---|---|
| `TELEGRAM_BOT_TOKEN` | Din bots token från @BotFather |
| `GEMINI_API_KEY` | Google AI Studio API-nyckel |
| `GUARDIAN_PASSPHRASE` | Unikt lösenord för föräldrars samtycke |

## Föräldrainstruktioner

Barnen är 10–12 år och faller under digital samtyckesålder (13 år i Sverige). **Samtycke måste ges innan barnet kan chatta.**

1. Öppna boten i Telegram
2. Skriv: `/consent [ditt-lösenord]`
3. Bekräfta att du tagit del av integritetsinformationen
4. Ditt barn kan nu skriva `/start` och börja!

För att återkalla samtycke: `/revoke` — all konversationsdata raderas.

## Dashboard

```bash
streamlit run dashboard/app.py
```

Logga in med samma lösenord som `GUARDIAN_PASSPHRASE`. Dashboarden visar:
- Antal meddelanden och aktiva dagar
- Senaste 50 konversationsturer (anonymiserade)

## Curriculum CLI

```bash
# Lista alla curriculumposter
python scripts/curriculum_cli.py list

# Validera att JSON-filerna har rätt format
python scripts/curriculum_cli.py validate
```

Lägg till fler Lgr22-data genom att skapa nya `.json`-filer i `config/lgr22/` med samma schema som de befintliga.

## Arkitektur

```
┌──────────────────┐
│  Telegram Bot     │  ← python-telegram-bot v21+
│  (barnet chattar) │
└────────┬─────────┘
         │
         ▼
┌──────────────────────────────────────────────────┐
│              skooli_buddy/core.py                 │
│                                                   │
│  1. Ladda child_profile + policies + lgr22-data  │
│  2. Bygg systemprompt (Sokratisk + Lgr22-kontext)│
│  3. Skicka till Gemini 2.5 Flash                 │
│  4. Enkel output-check                           │
│  5. Logga till JSONL                             │
└───────┬──────────────────────────┬───────────────┘
        │                          │
        ▼                          ▼
┌───────────────────┐   ┌─────────────────────────┐
│  Google Gemini    │   │  Föräldra-dashboard      │
│  2.5 Flash        │   │  (Streamlit)             │
│  Paid Tier 1      │   │  Läser JSONL-loggen +    │
│                   │   │  hanterar samtycke        │
└───────────────────┘   └─────────────────────────┘
```

## GDPR

- **Dataminimering:** Bara numeriskt `chat_id` sparas, aldrig namn eller personuppgifter
- **Samtycke:** Förälders samtycke krävs (GDPR Art. 8, barn under 13 år)
- **Rätt till radering:** `/revoke` raderar all data omedelbart
- **Datalagring:** Bara lokalt på din server, aldrig delat med tredje part
- **Gemini Paid Tier 1:** Google använder inte datan för modelträning

## Tester

```bash
python -m pytest tests/ -v
```
