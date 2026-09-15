# Plattformen — kernel föräldern äger

Arbetsnamn: **Skooli Buddy**. Namnet är inte låst.

> Föräldern styr sidekicken. Inte läroplanen. Inte skolan.
> Inte vi. Kernel är öppen. Allt ovanpå går att byta ut.

## Vad som är kernel, vad som är pack

```
  safety-kärna     kan inte stängas av     (BRIS, våld, sex, facit-först, hemligheter)
        │
  runtime          BYO-modell, ytor, logg, samtycke, tenant
        │
  packs            föräldern laddar / skriver / stänger av
                   pedagogik · världsbild · kursplan · röst · extra agenter
```

**Vendor lock-in är ett fel.** En förälder ska kunna:

- köra samma kernel hemma (Open) eller hos oss (Hem)
- byta modell (Ollama, egen nyckel, vår EU-nyckel)
- byta yta (WhatsApp, Telegram, PWA)
- exportera barnkort, logg, packs som vanliga filer
- **ladda upp egna agenter** (markdown: SOUL/SKILL-overlay) eller
  skriva en själv
- stänga av Lgr22 helt
- sätta en världsbild — inklusive tro, om det är *deras* val

Det vi säljer på Hem är drift och att kontakten hamnar i barnets
chatt. Inte en låst pedagogik. Inte en statlig kursplansmotor.

## Vem som inte får styra

| Aktör | Roll |
|-------|------|
| Förälder / vårdnadshavare | Operatör. Världsbild, packs, tid, yta, radering. |
| Barnet | Öppnar chatten självmant. Styr inte säkerhetskärnan. |
| Skolverket / Lgr22 | **Valfritt pack.** Default på för svenska läxor, av för den som inte vill. Aldrig överhet. |
| Skola, kommun, lärplatta | Ingen koppling. Inget tenant-träd "klass". |
| Vi (hosted) | Processor/drift. Inte livsåskådning. Inte nudging. |

Om en förälder vill att sidekicken väver in Gud i lärandet — det
är ett **världsbilds-pack de slår på**. Plattformen är inte ateistisk
och inte konfessionell. Den är förälderstyrd. Neutral är bara
default när föräldern inte valt.

Barnet kan inte jailbreaka in en annan tro för att köra över
föräldern. Föräldern kan inte luckra upp safety-kärnan
("inga regler", sexuellt, våld, hemligheter från vårdnadshavare).

## Pack-format (mål)

En pack är en mapp med markdown + manifest. Samma språk som
`agents/tutor/`. Föräldern släpper in den i `vault/packs/` eller
via Hem-panelen.

```
vault/packs/
  lgr22/           # valfri svensk kursplan
  worldview/       # förälder-skriven: tro, värderingar, språk hemma
  pedagogy/        # vilka metoder som får användas
  accommodations/  # det föräldern valt att berätta (diagnos, preferenser)
  custom-agent/    # egen SOUL/SKILL ovanpå kernel
```

`manifest.json`: id, namn, slår_på, av_förälder, version.
Kernel laddar packs **efter** safety. Konflikt mot safety = pack
vinner inte.

Export: zip av vault. Import på en annan maskin. Ingen molnplikt.

## Diagnos och preferenser

Vi sätter aldrig diagnos. Vi **lyssnar när föräldern berättar**.

Om föräldern skrivit "dyslexi", "adhd", "behöver pauser",
"läs högt först" — då anpassar sidekicken tyst: korta bitar,
en sak i taget, ingen skam, rätt metod från SKILL.

Vi nämner inte etiketten för barnet om inte föräldern bett om det.
Behov styr, precis som Skolverket säger — men källan till behovet
är hemmet, inte ett skolärende.

Tomt fält = extra-stöd-default åt alla. Ingen tvingas fylla i
diagnos för att få en bra sidekick.

## Intresse utan nudge

Inget "dags för matteläxan". Intresse hålls genom:

- flera lärandeformer (inte bara Sokrates) — se SKILL.md
- barnets egna intressen som bro, inte som muta
- korta svar, byte av metod när det kärvar
- leken och nyfikenheten är giltiga ingångar
- de öppnar chatten själva

Kreativt och lärorikt är kernelns jobb. Påminnelse-spam är inte
en feature vi "låser upp" bakom Hem.

Namnet **Skooli Buddy** är arbetsnamn. Bytenamn ska inte kräva
omskrivning av kernel — bara chattnamnet föräldern satt.

## Privacy

Bästa skyddet är minst data + förälderns nycklar.

- Dataminimering, revoke som tar allt, tenant per familj
- Hosted: EU, ZDR, PII bort före modell, DPIA
- Open: data lämnar inte hemmet om de kör Ollama
- Packs och diagnosanteckningar är extra känsliga — kryptas,
  exporteras bara till föräldern, aldrig till skola
- Inga trackers, ingen träning på barnchatt
