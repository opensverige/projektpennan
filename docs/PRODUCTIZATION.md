# Produktifiering — kernel, Hem, Auto

> Accounted: manuellt är gratis, kopplingarna kostar.
> Odysseus: kör själv, ta med egen nyckel om du vill.
> Vi: kärnan är fri. Vi tar betalt för att ge barnet den på fem minuter, säkert.

Det här är produkt-, design- och säkerhetsteamets gemensamma läsning
av repot. Inte en featurelista. En affärs- och leveransmodell.

## Tes

Skooli Buddy ska produktifieras som **öppen kernel + betald drift**,
inte som en stängd barn-app och inte som "klona och orka Docker".

| Analog | Vad vi lånar | Vad vi inte lånar |
|--------|----------------|-------------------|
| [Accounted](https://www.accounted.se/priser) | AGPL-motor alltid med. Open 0 kr. Auto ~199 kr för *kopplingar och drift*. Custom för white-label. BankID. "Föreslår, du godkänner." AI i EU. | Bokföringsmetaforen. Vi säljer inte till byråer. |
| [Odysseus](https://github.com/odysseus-dev/odysseus) | Self-host först. Lokal modell default. BYO OpenAI-compat. Auth på, porta inte ut. | Vi är inte ett vuxen-workspace. Inget shell, ingen mail-ingest. |
| [Lightdash-prissättning](https://mobbin.com/sites/sections/923ce9ff-1152-446a-8654-ce0b7ff3e537) | Tre kolumner: self-host / hosted / let's talk. | Enterprise-BI-språk. |

**Vad föräldern köper när de betalar:** inte pedagogiken (den är
öppen). De köper att *någon annan* håller boten vid liv, BankID,
EU-inference, support och att barnet kan börja kvällen utan att
pappa sätter upp Ollama.

**Vad som aldrig får bli betalt:** safety-kärnan, samtycke, revoke,
BRIS, Sokratisk default, extra-stöd-lägen, export av egen data.
Det vore att sälja barnets skydd.

---

## 1. Produkt — vad vi säljer

### Job to be done
När läxan kärvar en tisdag kväll ska en förälder kunna **ge barnet
en sidekick på fem minuter**, se vad som hände, pausa och radera —
utan skola, utan Docker, utan att barnet skaffar ett till socialt konto.

Self-host finns för den som vill äga allt. Det är trovärdigheten.
Det är inte volymvägen.

### Tre planer (Accounted-översättning)

| | **Open** · 0 kr | **Hem** · ~149–199 kr/mån | **Custom** · offert |
|---|-----------------|---------------------------|---------------------|
| Vem | Tech-förälder, granskare, bidrag | Vanlig familj | Kommun? Nej. Skola? Nej. Möjligen *familjekluster* / stödorganisation som self-hostar åt många hem. |
| Motor | Hela kernel, AGPL | Samma motor, vi driftar | Samma motor, er server eller vår |
| Barnchatt | Du sätter upp ytan | En länk. Klart. | Er domän |
| Modell | BYO: Ollama / egen nyckel | Vi betalar EU-inference. BYO-nyckel som tillval (då går data till *er* leverantör) | Valfritt |
| Identitet | Lösenord du väljer | BankID på föräldern | BankID / SSO åt vuxna, aldrig barn |
| Support | GitHub / Discord | Människa, vardagkväll | Egen kontakt |
| Extra | Du kopplar själv | Bild på läxa, veckomejl, andra ytor | White-label |

Priset ska kännas som **en timme läxhjälp per månad**, inte som
Netflix. 149–199 följer Accounteds Auto (199). Vi publicerar inte
slutpris här — vi publicerar *logiken*.

### Vad som är kernel (alltid öppet)

Det här är "BAS-planen" i Accounted-språk. Finns i git. Går att köra
hemma. Hosted *är samma kod*.

```
kernel/
  pedagogy     SOUL + SKILL + RULES (flera metoder, inget läx-nudge)
  safety       filter, kris→BRIS, jailbreak, sessiongräns   ← packs kan inte stänga av
  consent      ge / återkalla / radera
  profile      barn + support_preferences
  packs        kursplan / världsbild / pedagogik / anpassning / egen agent
  curriculum   Lgr22 som *pack*, avstängbart
  memory       lokalt, nollställbart
  log          JSONL + audit, dataminimerad
  providers    Ollama | OpenAI-compat | Gemini   ← BYO
  surfaces     web-PWA | Telegram | (senare WhatsApp)
  parent_api   paus, tid, läge, packs, export, revoke
```

Se [docs/PLATFORM.md](PLATFORM.md). Vendor lock-in på agent eller
livsåskådning är ett fel. Det vi säljer på Hem är drift.

Hosted lägger *utanpå* kernel: tenant-isolering, BankID, faktura,
vår modellnyckel, supportkö, uptime. Inte en fork.

### Vad Hem (Auto) tar betalt för

Accounted tar betalt för **bankkoppling, AI-kontering, Skatteverket**.
Vi tar betalt för analogerna:

| Accounted Auto | Skooli Hem |
|----------------|------------|
| PSD2-bank | Vi kör boten så den svarar kl 19 en tisdag |
| AI-kontering i EU | Inference i EU, ZDR, ingen träning |
| Kvitton via WhatsApp | Barnet skriver där de redan är (WhatsApp-kontakt) |
| "Föreslår, du godkänner" | Veckosammanfattning föräldern läser — aldrig betyg |
| Prioriterad support | Människa när något skaver |
| Flera användare | Två vårdnadshavare + ett barn (syskon = extra) |

Bild-på-läxa och röst är **tillägg eller Hem-plus**, inte kernel-lås.
Koden för dem ska ligga öppet. Driften (vision-API, transkription)
kostar oss pengar, därför kostar den familjen pengar *när vi hostar*.

### Vad vi medvetet inte säljer
- Skolkonto hos oss, Unikum-SSO, klasslista, lärarvy, write-back.
  Förälder-ägd minimerad skolkontext (lapp / lokal connector) är
  kernel, inte en kommundeal.
- Diagnosverktyg eller "NPF-paket" som sälj. Föräldern får *själv*
  skriva en anteckning; vi sätter aldrig etiketten.
- Reklam, affiliates, sälj av insikter
- Att *låsa* safety bakom paywall
- **Ett genererat `.md`-pack som checkout.** Vaulten *är* markdown
  (Obsidian-modellen). Filen är export och kvitto, inte SKU.
  Intaget på Hem ingår. **Kväll** är en tjänst för Open, inte
  en Gumroad. Se [docs/INTAKE.md](INTAKE.md).

---

## 2. Design — smidigt att ge barnet detta

### Kanaler, med data — inte magkänsla

Telegram är **lättast för oss** (redan byggt, Bot API, grupper).
Det är **inte** smidigast för svenska barn.

Internetstiftelsen 2025, barn 8–19:

- WhatsApp ~40 %
- Discord ~25 %
- Telegram / Signal: några få procent

Mediemyndigheten 2025: färre 9-åringar har egen mobil. Många
mellanstadiebarn gör läxan på **surfplatta i köket**.

Alltså:

| Yta | För vem | Friction | Säkerhet | När |
|-----|---------|----------|----------|-----|
| **WhatsApp-kontakt** | Barnet som redan har mobilen | Samma chattlista som kompisarna. Bild + röst de redan kan. | Meta ser meddelanden. Priset för att vara där de är. | **Hem-barn, default.** |
| **Förälder-PWA** | Vårdnadshavaren | BankID, paus, PIN. Aldrig på barnets skärm. | Högst. Vi äger den ytan. | **Hem-förälder, default.** |
| **Barn-PWA** | Ingen WhatsApp, gemensam iPad, vägrar Meta | Fallback. Inte en QR-ceremoni med barnet. | Högst. | Fallback, inte vardagsvägen. |
| **Telegram** | Tech-förälder, self-host | Få barn har det. | Medel. Icke-EU. | Open. Inte Hem-berättelsen. |
| Native app | Senare | Store-granskning, 13+ trassel | Bra om vi skippar trackers | Inte v1 |

**Produktbeslut:** barnet möter oss som **en kontakt i den chatt
de redan har** — i Sverige WhatsApp först. Inte en QR, inte en
ny flik, inte "nu ska du prata med AI:n". Se
[docs/UX-SCENARIOS.md](UX-SCENARIOS.md).

- **Hem-barn:** WhatsApp-kontakt (1:1). Föräldern lägger till den
  som mormor, tyst.
- **Hem-förälder:** web/PWA på *förälderns* telefon (BankID, paus, PIN).
- **PWA för barnet:** bara fallback (ingen WhatsApp, gemensam iPad,
  max integritet). Inte vardagsvägen.
- **Telegram:** Open / nördförälder. Inte Hem-berättelsen.

Meta som underbiträde är priset för att vara där de är. Det står
i samtycket. Open-core finns för den som vägrar.

### Anti-mönster (inte så här)

[Garmin Connects barnkonto](https://mobbin.com/flows/fac935c1-143a-43e5-861e-b1e65aa6d3a5)
tvingar **barnets e-post + lösenord**. Fel för oss. Barnet ska inte
ha ett konto. Föräldern är administratör till 13 — *den* meningen
hos Garmin är däremot rätt.

### Mönster vi tar

1. **Föräldern är admin till 13** — [Garmin](https://mobbin.com/flows/fac935c1-143a-43e5-861e-b1e65aa6d3a5) / [Meta Quest](https://mobbin.com/screens/dd94dbd9-2e7f-4bfe-a54e-0b2779aeb112)
2. **PIN på vuxen-ytan** — [Spotify Kids](https://mobbin.com/flows/1a3f9a8c-6ca2-45cd-aae7-7124088623ec). Barnet ska inte råka öppna loggen.
3. **Åldersband, inte diagnos** — [YouTube Kids 9–12](https://mobbin.com/flows/1d207d54-f174-40e3-9eaa-e14262000c47)
4. **Paus som förstaklass-handling** — [Revolut "Pause weekly allowance"](https://mobbin.com/screens/30c475b4-40dc-466b-b504-b2ac3ca3bfa2)
5. **Tidsgräns + påminnelse** — [Whatnot](https://mobbin.com/screens/d40efedd-3b9b-4193-99f5-11b30b8ca9f3), [YouTube](https://mobbin.com/screens/ccc65abb-f486-47ec-953e-2c6da12d1eee)
6. **Checklista "gör klart barnets setup"** — [Greenlight](https://mobbin.com/screens/7e97e03a-4c8e-47f3-8aab-2798ba5514ab) / [GoHenry](https://mobbin.com/screens/b40b68b8-c923-4155-8a8f-12983e659ad8)
7. **Blockerad innehållslista synlig** — [Spotify Kids](https://mobbin.com/screens/92060d61-ac33-4284-bc66-e4500cc46390)

### Hem-onboarding (föräldern, barnet är inte med)

```
1. Förälder   BankID på sin egen telefon. Barnen i sitt rum.
2. Samtycke   kort. Inklusive: "chatten går via WhatsApp/Meta."
3. Barnkort   tilltalsnamn, åk, stödpreferenser. Valfritt: det
              föräldern vill berätta (diagnos, ork). Aldrig krav.
4. Tid        45 min, 19:30 stopp. Inget läxalarm till barnet.
5. Yta        Default: "Lägg Skooli som kontakt i barnets WhatsApp"
              (samma gest som att lägga till mormor)
              Fallback: PWA-länk om det inte finns WhatsApp
6. PIN        på förälderns panel, inte i barnets chatt
7. Klart      Kontakten ligger där. Ingen demo med barnet i knät.
```

Barnet ser aldrig BankID, aldrig pris, aldrig loggen.
Första gången de skriver är första gången produkten "börjar".

### Föräldrayta (inte Streamlit, inte skolrapport)

En kvällsskärm:

- Status: igång | pausad | dagens tak nått
- Stor **Pausa**-knapp (Revolut-mönstret)
- Idag: antal turer, ämne, ett genombrott i klartext
- Vecka: enkel stapel, inte betyg
- Inställningar bakom PIN: tid, metoder, packs, världsbild, bilder
  på/av, yta, radera allt

Streamlit och `guardian.html` är proto. Hem v1 är en riktig
föräldra-PWA. Samma `parent_api` som Open använder lokalt.

---

## 3. Säkerhet — toppsäkert, två lägen

Self-host och hosted har **olika ansvar**. Blanda inte ihop dem.

| | Open (self-host) | Hem (vi driftar) |
|---|------------------|------------------|
| Personuppgiftsansvarig | Föräldern | **Vi** (B2C). Föräldern är registrerad / vårdnadshavare. |
| Underbiträden | De föräldern själv väljer (Ollama lokal = inga) | Vår host, vår LLM, ev. BankID-leverantör, ev. Telegram/Meta om ytan slås på |
| Krav innan första familj | README + SAFETY_SPEC | DPIA, DPA mot underbiträden, barnanpassad information, IMY-redo process |

### Hosted är en annan produktjuridiskt
Så fort vi kör kernel åt en familj behandlar vi barns uppgifter.
Då räcker inte "vi är open source". Innan Hem-lansering:

1. DPIA (barn + AI = högrisk)
2. Rättslig grund: vårdnadshavares samtycke (DSL 2:4, under 13)
3. Underbiträdeslista, EU-region, ZDR på LLM, ingen träning
4. PII-tokenisering *före* modell (namn, adress, skola, telefon)
5. Tenant-isolering per familj, kryptering i vila, korta retention
6. Export + radera som fungerar på *alla* kopior (logg, minne, backup)
7. Inget skol-id, ingen delning mellan familjer
8. Incidentplan, 72 h, vårdnadshavare först

### Threat model (kort)

| Hot | Öppen yta | Motmedel |
|-----|-----------|----------|
| Främmande barn hittar boten | Telegram/WhatsApp | Allowlist per familj. Default vägra. Inget publikt @skoolibot utan start-token. |
| Syskon gissar lösen | Dashboard | BankID + PIN. Inte `GUARDIAN_PASSPHRASE` i chatten. |
| Jailbreak / facit | LLM | Safety i *kod* före och efter. P-03. |
| Prompt injection via läxbild | Vision | Bild opt-in. Ansikten droppas. OCR-text genom samma filter. |
| Läckt JSONL / support-titt | Hosted | Roller, audit, minst-behörighet. Support ser inte chatt utan ticket + tidsbegränsad nyckel. |
| US-modell tränar på läxan | Gemini raw | Hem-default: EU + ZDR. BYO = föräldern kryssar "jag skickar till *min* leverantör". |
| Telegram läser allt | Telegram-yta | Informerat val. PWA default just för att undvika det. |
| Kris missas | Prompt-only BRIS | Kod-trigger, logga `blocked/crisis` till förälder (inte innehållet i push). |
| Vi blir skol-leverantör av misstag | Säljtryck | Inget tenant-träd "klass". En familj = en tenant. |
| Läckt diagnospack | Hosted / support | Art. 9. Krypterat i vila (P-36). Support ser aldrig labels. Aldrig till skola. |
| Pack stänger safety | Upload | Manifest `cannot_override_safety`. Konflikt = pack vinner inte. |

### BYO (Odysseus-läget)
Föräldern klistrar in egen nyckel i Hem *eller* i Open.

- Vi lagrar nyckeln krypterad, per tenant, aldrig i logg
- UI: "Då lämnar barnets text *din* leverantör. Vi kan inte lova EU."
- Safety-kärnan körs fortfarande hos oss / lokalt *före* anropet
- Open: nyckeln stannar i `.env` på deras disk

Lokal Ollama förblir det privataste. Hem ska inte *tvinga* moln —
den som vill kan peka Hem mot en URL de själva kör (Tailscale).
Det är Custom-känsla, men en toggle räcker för nördar.

### Telegram-specifikt (om ytan är på)
- Ingen global bot som tar emot vem som helst
- `t.me/skoolibot?start=<engångstoken>` bunden till familj, TTL 15 min
- Bara allowlistad `chat_id` efter att föräldern bekräftat i BankID-ytan
- Ingen lagring av username, foto, telefon
- Grupper: förälder spectator, bot svarar bara barnet — explicit läge

---

## 4. Arkitektur som matchar affären

```
                 Open     Docker / hem-NUC / Ollama
                    \
  kernel (AGPL)  ----+---- Hem      vår drift, BankID, EU-LLM
                    /
                 ytor     PWA | Telegram | WhatsApp-adapter
```

Samma `get_response` / `parent_api`. Inga två sanningar
(det är P-01). Hosted är config + identitet + faktura.

Repo-riktning (inte gör allt nu):

```
skooli_kernel/          # pedagogy, safety, consent, providers
surfaces/web/           # barn-PWA + förälder-PWA
surfaces/telegram/      # dagens skooli_buddy/bot.py, slimmad
surfaces/whatsapp/      # senare
hosted/                 # tenant, bankid, billing — kan vara stängt
                        # men ska kalla kernel, inte forka den
```

`hosted/` *får* vara sluten operationskod (secrets, terraform)
så länge kernel inte urholkas. Accounted håller motorn öppen och
säljer kopplingar. Vi gör likadant: billing och BankID-adapter
kan vara "Hem-repo", men safety får inte flytta dit.

---

## 5. Prissida (copy-riktning)

Ton: Accounted + Lightdash. Tre kort. Inget "Pro för power-users"
som låser skydd.

**Open — 0 kr**
Kör hela motorn hemma. AGPL. BYO-modell. Community.

**Hem — mest vald**
Vi slår på den åt er. BankID. Barnlänk. EU-modell. Pausa-knapp.
30 dagar, sen en läxhjälpstimme i månaden.

**Egen drift**
Er server, vår hjälp. För den som inte vill att vi ser något.

Jämförelsetabell som Accounted: kernel-rader alltid bockade.
Hem-rader: BankID, vi-driftar, EU-inference, support, extra ytor.

---

## 6. Byggordning mot produkt

P0–P1 i `docs/BACKLOG.md` står kvar. Produktifiering lägger:

| ID | Vad |
|----|-----|
| P-25 | **Kernel-gräns.** Dela kod så hosted bara är tenant+identitet+faktura. |
| P-26 | **Provider-adapter.** Ollama / OpenAI-compat / Gemini bakom samma interface. BYO. |
| P-27 | **Förälder-PWA.** PIN, paus. Inte barnets vardagsyta. |
| P-28 | **Webb-först onboarding.** Samtycke, form, modell, yta. BankID bara på Hem. |
| P-29 | **DPIA + underbiträden + ZDR-policy** innan första betalande familj. |
| P-30 | **Telegram start-token + allowlist** (ersätter hårdkodat id). Open *och* Hem. |
| P-31 | **Prissida + DPA-text** i docs, Accounted-struktur. Open / Hem / Kväll. Inte en pack-butik. |
| P-32 | WhatsApp-yta som Hem-koppling, inte som identitet. |

Ordning som gör "ge barnet detta" sant:

1. P-01 + P-03 + P-26 — en motor, safety i kod, BYO
2. P-32 + P-30 — WhatsApp-kontakt (Hem-barn) + säker allowlist
3. P-27 — förälder-PWA (paus, PIN), inte barnets destination
4. P-28 + P-29 — då först ta betalt (Meta i DPIA)

Att sälja Hem på dagens Telegram-bot med hårdkodat chat-id vore
att produktifiera en labbuppställning.

---

## 7. Beslut att låsa nu

1. **Open-core, inte open-core-teater.** Kernel = allt som skyddar
   och undervisar. Hem = drift + identitet + inference vi betalar.
   Intaget ingår i Hem. `.md` är export, inte butik (P-46).
2. **Kontakt i WhatsApp först för barnet.** Föräldern har PWA.
   Telegram är Open. Barn-PWA är fallback, inte ceremoni.
   Inget läxpush. Inget "nu ska du prata med AI:n".
3. **Barnet har inget konto.** Föräldern är admin till 13.
4. **BankID på vuxen, PIN på panelen.** Inget barnlösen i chatten.
5. **Ingen skola i tenant-modellen.** En familj, en vault.
6. **BYO alltid möjligt.** Hosted default är EU-ZDR som vi betalar.
7. **Inte ta betalt förrän DPIA och safety-i-kod finns.**
