# Produktvision — Skooli Buddy

> En sidekick i barnets ficka. Spakarna hemma. Aldrig skolans system.
> Kontaktnamn: Utter. Initiativ: Projekt Pennan.
> Kernel föräldern äger — inte en låst app. Se `docs/NAME.md`.

## Vem vi bygger för
- Barn 9–12 år (åk 4–6 först) som behöver **stöd, inte mer press**.
- Vårdnadshavare som vill hjälpa till med läxor utan att sitta
  bredvid varje kväll — och utan att lämna data till skolan.
- Familjer som inte har råd med 600 kr/timme i läxhjälp.
- **Byggar- och viber-föräldrar** som redan slänger ihop en GPT,
  en vault eller ett script mot skolplattformen — de ska kunna
  släppa in det i samma kernel, inte börja om.

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

Det är läxhjälp + extra anpassning + trygg vuxen-insyn, i chatten
barnet redan har. Föräldern kan byta världsbild, metoder och agenter.
Läroplanen styr inte. Se [docs/PLATFORM.md](PLATFORM.md).

## Varför inte skolan i mitten
Skolans digitala kedja (lärlogg, Unikum, Google-konto, kommunmoln)
är byggd för administration. Den är dålig på:

- barnets integritet mot en stor organisation,
- förälderns rätt att säga nej,
- barn som behöver stöd *utan* att det blir ett ärende.

Skooli Buddy är ett **hemverktyg**. Föräldern är personuppgiftsansvarig
när de kör det själva. Vi ger dem koden, reglerna och en lokal
default. Vi kopplar inte barnet till ett skol-id. Skolan får vara *källa*
om föräldern själv hämtar och minimerar (ämne + tema, inte betyg).
Se [docs/PLATFORM.md](PLATFORM.md).

## Lärandeformer vi står för
Bygger på research i `research/findings/`:

| Form | Vad det betyder här | Källa |
|------|---------------------|-------|
| Sokratisk dialog | Motfråga, inte facit | RCT på Socratic AI i K–12; Khanmigo-linjen |
| Scaffolding | Små steg, tänka högt, ta bort stöd | Explicit instruction + fading |
| UDL | Flera sätt att förstå / svara / orka | CAST; SNUDLE |
| Extra anpassning | Behov default; diagnos bara om *föräldern* skrivit den | Skolverket, SPSM |
| Visat exempel / CPA | Likadant tal; äpplen → streck → siffror | Sweller; NCETM |
| Saga och lek | Kreativ ingång, inte läx-nudge | UNICEF Learning through Play |
| Hämtning ur minnet | Bara när barnet vill köras | Retrieval practice |
| Världsbild | Förälderns pack, inklusive tro | Barnkonventionen art. 14 |
| Separera avkodning och innehåll | Textuppgifter i två lager | SPSM dyslexi-stöd |
| Kort session + synligt framsteg | Ork och NPF | Skolverket NPF-lärmiljö |
| Kris = människa | BRIS, ingen chatbot-terapi | Safety spec |

## Konkurrentkarta (2026)
Ingen öppen, svensk, föräldrastyrd kernel-sidekick finns. Lgr22 är
ett pack hos oss, inte överhet.

| | Svenska + valfri kursplan | Aldrig facit | Förälder styr | Lokal / OSS | Messaging |
|---|---------------------------|--------------|---------------|-------------|-----------|
| **Utter** | Lgr22 som pack | ja | ja (mål) | ja | kontakt i chatt |
| Homework Buddy | Lgr22 inbakat | delvis | nej | nej | app |
| Pluggis | skolans material | ja | nej | nej | app |
| Allakando AI-lärare | svensk skola | delvis | nej | nej | webb |
| Studybuddy / Allakando | människa, 400 kr/h | — | nej | nej | — |
| Khanmigo | nej | ja | delvis, US/skola | nej | nej |
| ChatGPT / Gemini raw | nej | nej | nej | nej | ja |
| Skolon AI-studiehjälp | ja, skolkedja | varierar | nej | nej | app |

Vår kant: **öppen kernel + föräldern som operatör + extra stöd som
default + egna agenter**. Inte en låst läroplansapp. Inte Khan Academy.

## Hur det produktifieras
Öppen kernel, betald drift. Mall: [Accounted](https://www.accounted.se/priser)
(Open 0 kr / Auto ~199 / Custom) + Odysseus BYO-nyckel.

- **Open:** hela motorn hemma, Docker, egen modell.
- **Hem:** vi slår på den på fem minuter. BankID. Skooli som
  tyst WhatsApp-kontakt hos barnet. Föräldrapanel på *er* telefon.
  PWA bara som fallback. EU-inference.
- **Egen drift:** er server, vår hjälp.

Pedagogik och safety är aldrig paywall. `.md`-packen är export,
inte checkout. Detalj: [docs/PRODUCTIZATION.md](PRODUCTIZATION.md),
[docs/PRICING.md](PRICING.md), [docs/INTAKE.md](INTAKE.md).

## Nordstjärna för v1.0
En förälder i Sverige kan på fem minuter (Hem) eller en kväll (Open):

1. BankID *eller* klona/köra image,
2. ge samtycke, sätta tid, metoder, ev. världsbild och ev. anpassning,
3. lägga sidekicken som en tyst kontakt i barnets WhatsApp
   (PWA bara som fallback — inte en QR-ceremoni),
4. se, pausa, exportera, byta pack eller radera.

Inget skolkonto hos oss. Ingen klass. Ingen molnplikt på Open.
Lgr22 av om de vill. Egna agenter in om de vill.
Veckans skolteman in om de vill — som en lapp, inte som Unikum.
