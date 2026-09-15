# Produktvision — Skooli Buddy

> En sidekick i barnets ficka. Spakarna hemma. Aldrig skolans system.

## Vem vi bygger för
- Barn 9–12 år (åk 4–6 först) som behöver **stöd, inte mer press**.
- Vårdnadshavare som vill hjälpa till med läxor utan att sitta
  bredvid varje kväll — och utan att lämna data till skolan.
- Familjer som inte har råd med 600 kr/timme i läxhjälp.

Vi bygger **inte** för rektorer, kommuner, lärplattformar eller
EdTech-upphandlingar. Om skolan vill rekommendera oss är det bra.
De får inte drifta oss.

## Jobbet vi gör
När läxan kärvar ska barnet kunna fråga en kompis som:

1. aldrig ger svaret,
2. anpassar tempot,
3. tål "jag är dum" utan att hålla med,
4. stannar när det blir jobbigt,
5. syns för föräldern.

Det är läxhjälp + extra anpassning + trygg vuxen-insyn, i en app
familjen redan använder (Telegram nu, lokal web och fler ytor sen).

## Varför inte skolan i mitten
Skolans digitala kedja (lärlogg, Unikum, Google-konto, kommunmoln)
är byggd för administration. Den är dålig på:

- barnets integritet mot en stor organisation,
- förälderns rätt att säga nej,
- barn som behöver stöd *utan* att det blir ett ärende.

Skooli Buddy är ett **hemverktyg**. Föräldern är personuppgiftsansvarig
när de kör det själva. Vi ger dem koden, reglerna och en lokal
default. Vi kopplar inte barnet till ett skol-id.

## Lärandeformer vi står för
Bygger på research i `research/findings/`:

| Form | Vad det betyder här | Källa |
|------|---------------------|-------|
| Sokratisk dialog | Motfråga, inte facit | RCT på Socratic AI i K–12; Khanmigo-linjen |
| Scaffolding | Små steg, tänka högt, ta bort stöd | Explicit instruction + fading |
| UDL | Flera sätt att förstå / svara / orka | CAST; SNUDLE |
| Extra anpassning | Behov, inte diagnos | Skolverket, SPSM |
| Separera avkodning och innehåll | Textuppgifter i två lager | SPSM dyslexi-stöd |
| Kort session + synligt framsteg | Ork och NPF | Skolverket NPF-lärmiljö |
| Kris = människa | BRIS, ingen chatbot-terapi | Safety spec |

## Konkurrentkarta (2026)
Ingen öppen, svensk, Lgr22-kopplad, föräldrastyrd sidekick finns.

| | Svenska + Lgr22 | Aldrig facit | Förälder styr | Lokal / OSS | Messaging |
|---|-----------------|--------------|---------------|-------------|-----------|
| **Skooli Buddy** | ja (tunnt) | ja | delvis | ja | Telegram |
| Khanmigo | nej | ja | delvis, US/skola | nej | nej |
| Sorin / Tutur / Latio | nej | ja | ja, stängt | nej | app |
| ChatGPT / Gemini raw | nej | nej | nej | nej | ja |
| Skolans "AI-assistent" | ev. | varierar | nej | nej | nej |

Vår kant: **svenska + öppen kod + föräldern som operatör + extra stöd
som default**. Inte fler features än Khan Academy.

## Nordstjärna för v1.0
En förälder i Sverige kan på en kväll:

1. klona repot eller köra en image,
2. ge samtycke,
3. sätta tid, stödläge och ämnen,
4. låta barnet chatta i Telegram *eller* i webben mot lokal modell,
5. se vad som hände, exportera eller radera.

Inget skolkonto. Ingen klass. Ingen molnplikt.
