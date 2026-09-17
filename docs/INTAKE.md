# Intag — sälj kvällen, inte filen

> Tes som utmanas: *sälj att plattan blir det här barnet i kväll
> (Hem), inte .md-packen.*
>
> Fynd: `research/findings/intake-not-file.json`.
> Prislogik: `docs/PRICING.md`.

Det här är inte en wizard-spec. Det är SKU-gränsen.

## Svar på frågan

**Ett genererat .md-pack som publik checkout-rad är en
one-shot-återvändsgränd.** Inte för att markdown är värdelös —
vaulten *är* markdown, som Obsidian — utan för att filen är
biprodukten av ett jobb, inte jobbet.

Jobbet: *plattan blir det här barnet och stannar på.*

Hem är rätt volym-SKU. Den är ofullständig om vi låtsas att
intaget inte finns, och den är farlig om recurring-avgiften
bara är natt ett utsmetad över tolv fakturor.

---

## Analogerna, från prissidor (2026-09)

| Analog | Vad de säljer | Vad de *inte* säljer | Lärdom |
|--------|----------------|----------------------|--------|
| [Accounted /priser](https://www.accounted.se/priser) | Open 0 kr (hela AGPL-motorn). Auto **199 kr/mån**, 30 dagar: PSD2, AI i EU, WhatsApp-kvitton, Skatteverket. Custom offert. Inhouse från **19 999 kr**. | En SIE-fil. "Migrering in" ingår i Open *och* Auto. | Betala när *kopplingarna* ska på. Intaget är inkluderat. |
| [Linear /pricing](https://linear.app/pricing) + [migration](https://linear.app/switch/migration-guide) | Free 0 / Basic 10 / Business 16 USD/säte/mån. Import/export är kärnrad. | Zippen. "Migration & onboarding support" bara på **Enterprise**. | Självbetjäningsimport är CAC. Människa som sätter upp är enterprise. |
| [Notion /pricing](https://www.notion.com/pricing) + [Marketplace](https://www.notion.com/help/selling-on-marketplace) | Free 0 / Plus 10 / Business 20 USD/säte/mån. AI på Business. | Mallar. Creators säljer mallar; Notion tar 8 % + 0,40 USD och kräver support. | Plattformen säljer säten. Fil-SKU:n är *andras* one-shot. |
| [Obsidian /pricing](https://obsidian.md/pricing) | Vault **gratis**. Sync 4 USD/mån årsvis (5 månadsvis). Publish 8/10. Catalyst 25 USD en gång. | Anteckningsfilerna. | Sälj sync, inte vaulten. .md är det de *ger bort*. |
| [Khanmigo /pricing](https://khanmigo.ai/pricing) | Lärare 0. Familj/elev **4 USD/mån eller 44 USD/år**, USA. | En barnprofil-fil. Innehållsbiblioteket förblir gratis. | Pågående tutor på en gratis motor. Nonprofit-golv, inte vårt WTP-tak. |
| [Aristotle /pricing](https://www.heyaristotle.com/pricing) | Intro: 3 gratissessioner. Scholar **49 USD/mån** (8 sessioner). Infinite **199 USD/mån** obegränsat. | En onboarding-fil. Sluggen `/why-aristotle-costs-299` lever; **listpriset är 199**. | De säljer en mätare som tickar (sessioner). Intaget är tre gratis. |
| [Nabu Casa](https://www.nabucasa.com/pricing/) | EU **7,50 EUR/mån** eller 75 EUR/år. | Home Assistant-installen. | Öppen motor, betald *daglig* koppling (fjärr + röst). |
| [n8n /pricing](https://n8n.io/pricing/) | Community 0 (self-host). Cloud Starter **20 EUR/mån** årsvis. | Workflow-JSON som produkt. | Samma split: kör själv gratis, betala för drift. |
| [Stripe Atlas](https://stripe.com/atlas) | **500 USD** engångs + ~100 USD/år registered agent. | En bolagsmall att fylla i själv. | One-shot *fungerar* när utfallet är juridiskt unikt. |
| [Superhuman onboarding](https://blog.superhuman.com/the-fastest-way-to-inbox-zero-a-single-coaching-session/) | Starter **25 USD/mån** årsvis / 30 månadsvis. 30 min 1:1 **ingår**. | En "inbox.md". | Vit handske inbäddad i ytan som fortsätter kosta. |
| [Allakando](https://www.allakando.se/laxhjalp-pris/) | Människa från **399 kr/t**. Grupp från 189. AI-lärare **gratis**. | En studieplan-fil. | Svenskt tak. En Kväll är timmar, inte 49 kr för zip. |
| [Homework Buddy](https://homeworkbuddy.app/en/pricing) | Gratis 3 samtal/vecka. Premium **3 EUR/mån** eller 18 EUR/år. | OSS, förälder-ägd kernel. | Race-to-bottom. Inte vår analog för pris. |

---

## När betalt intag fungerar

1. **Artefakten körs.** Linear-issues lever i Linear. Superhumans inbox
   är uppsatt *i* Superhuman. Accounted har flyttat verifikaten.
   Stripe Atlas har ett org.nr. Ingen av dem mailar en fil och går.
2. **Något tickar efter natt ett.** PSD2-transaktioner, Sync mellan
   enheter, sessioner (Aristotle), inference vi betalar, WhatsApp-yta,
   veckolapp med TTL (P-37). Prenumerationen betalar *det*, inte
   profilen.
3. **Arbetet är mänskligt och ansvarigt.** Enterprise-migration,
   Superhuman-coach, Accounted Inhouse, Allakando-timme. Köparen
   köper omdöme, inte tokens.
4. **Utfallet är svårt att göra själv *och* unikt.** Atlas 500 USD:
   Delaware + EIN + 83(b). En barn.md som en LLM skriver om på
   trettio sekunder är inte det.
5. **Upprepning.** Syskon, nytt läsår, ny ork, ny `THIS_WEEK.md`.
   Intaget dör inte efter första zippen.
6. **Köparen kan inte bedöma kvalitet förrän det lever.** "I kväll"
   är verifieringen. Filen går inte att prova.

## När det faller

1. **Statisk, kopierbar, regenererbar fil.** Notion-mallar 12–49 USD,
   Gumroad-promptar, character cards. AGPL + `vault/packs/`-mallar
   betyder att de redan *har* generatorn.
2. **Samma repo kan skriva packen.** Att ta betalt för output från
   en öppen mall är teater. Föräldern (eller ChatGPT) fyller
   `barn.md` själva.
3. **Inget jobb efter nedladdning.** One-shot NPS: de fick zipt,
   de försvann. Chargebacks äter marginalen (Notion håller 14 dagar
   just därför).
4. **Barndata i en fil utan controller-relation.** Art. 9 om
   anpassningar. Vi blir behandlare utan tenant, eller föräldern
   klistrar in packen i ChatGPT och kringgår plattan.
5. **Fel jobb.** Föräldern vill att tisdag kväll ska fungera, inte
   äga en markdown. "Pack" låter innehåll. Jobbet är omsorg + drift.
6. **Kannibalerar Hem.** Betalad fil → varför prenumerera?
7. **Hem som bara är uppsättning.** Om månad 2–12 inte har en
   mätare (inference, kontakt, veckolapp, människa) har vi sålt
   en engångsavgift i prenumerationskläder. Det är den fällan
   Accounted *undviker* genom att ta betalt för kopplingar som
   eldar varje dag.

---

## Utmaning av "bara Hem i kväll"

Slogans är rätt om *jobbet*. Den är fel som *enda* betalda SKU.

**1. Hem är inte byggt.** DPIA, BankID, WhatsApp Business, tenant
(P-29, P-32). Att sälja en prenumeration vi inte kan leverera är
värre än att sälja en fil. En **Kväll** (90 min människa + körande
lokal vault) kan säljas till byggarföräldrar *nu*, utan att vi
blir personuppgiftsansvariga.

**2. Recurring måste överleva natt ett.** Accounted Auto fungerar
för att banken spottar rader varje dag. Ett barnkort är nästan
statiskt efter vecka ett. Hem *måste* sälja det som tickar:
EU-inference vi betalar, tyst kontakt, paus, veckosammanfattning,
levande `THIS_WEEK.md`. Annars är 199 kr/mån en uppsättningsavgift.

**3. Hög WTP är människa, inte zip.** Aristotle Infinite 199 USD/mån
(tidigare kommunicerat 299). Allakando 399 kr/t. En förälder som
redan köper läxhjälp betalar hellre 1 190 kr för en kväll som
lämnar en *körande* Open-install än 49 kr för `barn.md`.
Khanmigo 4 USD och Homework Buddy 3 EUR är golv för stängd
innehålls-AI, inte tak för oss.

**4. Linear, inte Notion-creator.** Linear ger bort importen så att
sätet börjar kosta. Notion *själv* säljer inte mallar — creators
gör det, och det är en läckande hink. Kopiera Linear in i Hem.
Kopiera inte Gumroad.

**5. Filen är ändå helig — som export.** Obsidian tar inte betalt
för vaulten. GDPR art. 20 kräver portabilitet. P-33:s zip är
*kvitto och exit*, inte SKU. Att kalla filen värdelös vore att
svika Open. Att sätta den i checkout vore att svika Hem.

**6. Intag utan drift är tjänst, inte produkt.** Superhuman
bäddar in 30 min i prenumerationen. Accounted bokar 30 min för
att *flytta in i Auto*. Stripe Atlas tar 500 USD för att ett
bolag ska *finnas*. Vi tar betalt för Kväll bara när Hem inte
är vägen (Open / pre-DPIA). Vi tar inte betalt två gånger.

---

## Rekommenderad SKU-tabell

Svensk AGPL-barn-tutor. Safety, samtycke, BRIS, Sokratisk default,
världsbild, egen agent och att stänga av Lgr22 är **aldrig** paywall.

| SKU | Pris | Vem | De köper | De köper *inte* | Analog |
|-----|------|-----|----------|-----------------|--------|
| **Open** | **0 kr** | Tech-förälder, granskare | Hela kernel, pack-*format*, tomma mallar, Docker, BYO, community | Vår inference, BankID-som-controller, WhatsApp vi driftar, människa | Accounted Open. Obsidian vault. n8n Community. |
| **Hem** | **149–199 kr/mån**, 30 dagar | Vanlig familj | Plattan blir *det här* barnet **i kväll och stannar på**: tenant, BankID, EU-ZDR vi betalar, tyst WhatsApp-kontakt, förälder-PWA, paus, veckolapp, människa. Intaget ingår. | Pedagogiken. Skyddet. `.md` som produkt. | Accounted Auto 199. Superhuman (onboard ingår). Nabu Casa. Aristotle Scholar/Infinite som *mätar*-referens, inte pris. |
| **Kväll** | **0 på Hem.** **790–1 490 kr** engång för Open | Byggare som vägrar hostat, eller intäkt *före* DPIA | 90 min människa: chipintervju (P-45), vault skriven, Docker/Telegram igång, zip som **kvitto** | `barn.md` i en butik. Prenumeration vi inte kan hålla. | Superhuman 30 min *inbäddad*. Linear Enterprise = människa. Allakando-timmar. Atlas bara om utfallet är unikt — här är utfallet *körning*, inte fil. |
| **Syskon** | **+49–79 kr/mån** på Hem | Andra barnet i samma hushåll | Andra *körande* plattan | Rabatterad fil | Khanmigo 4 USD täcker många barn — för billigt för vår kostnad. En tenant till. |
| **Egen drift** | Offert. Inhouse-känsla från **~20 000 kr** | Familjekluster / org som self-hostar | Vi hjälper dem hosta. Samma kernel. | Skolavtal, klass-tenant | Accounted Custom / Inhouse 19 999. |

### Regler som låser SKU:erna

1. Checkout-raden får aldrig heta "barn.md" eller "profilpack".
2. Generatorn stannar i git. Tomma mallar i `vault/packs/` är Open.
3. Hem-intag = inkluderad labor (Linear-import, Accounted 30 min,
   Superhuman-coach).
4. Kväll faktureras som **tjänst**, inte digital download. Ingen
   automatisk zip-butik. Ingen Gumroad.
5. Hem måste ha minst en tickande kostnad vi faktiskt bär
   (inference och/eller WhatsApp och/eller människa). Annars
   sänk priset till en setup-avgift och sluta kalla det månad.
6. Export-zip är gratis på båda planer (art. 20, P-33).
7. Inte en krona på Hem innan P-03 + P-29.

Hur intaget *frågar* (chipordning) är ett annat fynd.
Den här filen är vad intaget *får kosta*.
