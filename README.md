# Skooli Buddy

> En personlig AI-studiekompis för svenska barn i åk 4–6. Bor i er Telegram-grupp. Ger aldrig svaret.

**Projekt Pennan** är ett open-source-initiativ under [opensverige](https://github.com/opensverige) som bygger AI-verktyg för svensk utbildning. Skooli Buddy är den första produkten.

---

## Vad är det?

Barnet (9–12 år) chattar med Skooli Buddy i Telegram. Boten använder **Sokratisk pedagogik** — den löser aldrig uppgiften, utan leder barnet mot egna insikter genom frågor och ledtrådar. All pedagogik är kopplad till svenska kursplanen (Lgr22).

Föräldern sitter med i samma Telegram-grupp som **spectator** och ser allt i realtid.

```
Barn: "Vad är 7 gånger 8?"
Skooli: "Vet du vad 7 gånger 7 är? Då kan vi räkna ett steg till! 🤔"
```

---

## Stack

| Del | Teknologi |
|-----|-----------|
| Bot | Python + python-telegram-bot v21+ |
| AI | Google Gemini 2.5 Flash (Paid Tier 1) |
| Föräldrapanel | Streamlit |
| Loggning | JSONL (GDPR-minimerat) |
| Kursplan | Lgr22-data i `config/lgr22/` |

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

Det här är en levande produkt. Planerade steg i prioritetsordning:

### v0.2 — Föräldrainsyn i realtid
- [ ] Telegram-grupp med förälder som passiv spectator (ser allt, kan inte störa)

### v0.3 — Bildstöd
- [ ] Barnet fotar läxan → boten läser bilden och ställer frågor
- [ ] Bildgenerering för pedagogiska bilder (klockor, geometriska former, enkla diagram)

### v0.4 — Minne
- [ ] Boten minns barnet mellan sessioner (intressen, var vi slutade, genombrott)

### v0.5 — Fler plattformar
- [ ] WhatsApp-stöd

### v1.0 — Bredare kursplan
- [ ] Fler årskurser (åk 1–3, åk 7–9)
- [ ] Matematisk verifiering av svar

---

## GDPR

- **Dataminimering:** Bara numeriskt `chat_id` sparas — aldrig namn eller personuppgifter
- **Samtycke:** Förälders samtycke krävs (GDPR Art. 8, barn under 13 år)
- **Rätt till radering:** `/revoke` raderar all data omedelbart
- **Datalagring:** Bara lokalt på din server, aldrig delat med tredje part
- **Gemini Paid Tier 1:** Google använder inte datan för modellträning

---

## Varför Skooli Buddy?

Ingen konkurrent kombinerar:
- Svenska + Lgr22
- Sokratisk metod (aldrig raka svar)
- Föräldrainsyn i realtid
- Messaging-native (Telegram/WhatsApp — där barnen redan är)

Khanmigo är närmast — men saknar svenska, Lgr22 och föräldrainsyn.

---

## Bidra

Vi välkomnar bidrag! Projekt Pennan är en del av [opensverige.se](https://opensverige.se) — ett community för open-source-verktyg på svenska.

```bash
git checkout -b feat/din-feature
# Gör dina ändringar
python -m pytest tests/ -v
git push origin feat/din-feature
# Öppna en PR mot main
```

Frågor? Öppna ett issue på [github.com/opensverige/projektpennan](https://github.com/opensverige/projektpennan) eller besök [opensverige.se](https://opensverige.se).

---

## Tester

```bash
python -m pytest tests/ -v
```

---

*Projekt Pennan — AI för svensk utbildning, byggt öppet.*
