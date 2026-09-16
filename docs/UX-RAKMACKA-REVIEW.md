# UX-review — räkmackan som Markov-kedja

Telegram går **inte** att testa i den här miljön. Den här
granskningen är därför tillstånd + felvägar, inte en live-bot.
Klickbar ersättning: `frontend/rakmacka.html`.

Markov-effekten: föräldern minns bara *den här* skärmen. Varje
övergång har en chans att de lämnar. Ett tillstånd som antar att
de “redan kryssade samtycke där borta” är ett hål.

```
S0 öppna       → S1 agent     → S2 barn      → S3 kontext
     │                │              │               │
   fel person      ingen check    tomt namn      klistrar Unikum
     ▼                ▼              ▼               ▼
   S0-barn         blockerad      blockerad      varning / strip

S3 ──skip──► S4 invite ──► S5 väntar ──► S6 barnet skriver
                  │              │
            iOS död / läckt   48 h / syskon
                  ▼              ▼
            S4-fallback      S5-utgången
```

Lyckat slut är **S6**, inte S4. Invite skickad är inte klart.
[ElevenLabs tom inbox](https://mobbin.com/screens/e17c50ee-c2b2-4e18-be49-32a057df3c2c)
och [Instacart pending + expire](https://mobbin.com/screens/8d07b218-a873-45f9-999b-c7ba70c24705)
visar samma sak: “invited” är ett eget tillstånd.

---

## S0 — öppna länken

| Kan gå fel | Effekt | Åtgärd |
|------------|--------|--------|
| Barnet öppnar `?startapp` | Barn sätter agent/tro/kontext | Mini App bara om `from` = förälder som startade. Barn som öppnar: “Be en vuxen.” Inte wizard. |
| Annan vuxen (lärare, moster) | Fel operatör | Checkbox räcker inte mot socialt tryck. Visa: “Bara vårdnadshavare. Inte skolan.” |
| Gammal Telegram / Mini App av | Tom skärm | Fallback: vanliga knappar i 1:1. Säg det på första raden. |
| Hårdkodat `ALLOWED_CHAT_ID` | Alla utom en tystas | P-02. Annars är räkmackan död för alla utom oss. |
| Bot blockad / privacy | Ingen update | Time-out-text: “Telegram släppte inte in oss. Öppna botten i 1:1.” |

Markov: S0 är det största läckaget. En länk i en skolchatt = fel kedja.

---

## S1 — agent

Chips är rätt ([ChatGPT Customize](https://mobbin.com/flows/a3659710-c1a1-48b4-bbdb-505f969cb856)).
Vad som går fel:

| Kan gå fel | Åtgärd |
|------------|--------|
| Ingen checkbox, trycker vidare | Fortsätt disabled. Inte en toast efteråt. |
| Väljer “tro” av nyfikenhet | En rad under: “Det här följer *er* tro. Barnet kan inte byta.” |
| “Egen” utan fil | Egen = “klistra 3 rader” eller hoppa till default extra-stöd. Inte en upload-ceremoni. |
| Back från S2 nollar valet | Spara state. Markov: de kommer inte skriva om. |

---

## S2 — barn

[Jomo](https://mobbin.com/screens/4a5679f7-4ece-4887-a703-c3de1c21f987) tar e-post. Vi får inte.

| Kan gå fel | Åtgärd |
|------------|--------|
| Efternamn / personnummer i fältet | Placeholder “bara tilltalsnamn”. Klipp vid mellanslag + varning. |
| Två barn | Inte i v1. En mening: “Ett barn nu. Syskon sen.” |
| Tomt / emoji-namn | Disabled. |
| Åk utanför 4–6 | Tillåt, men säg “vi är bäst på 4–6”. Inte ett stopp. |

---

## S3 — kontext

Skip måste vara förstaklass ([Bumble Skip](https://mobbin.com/screens/c040d441-e2e8-4502-92f8-7b806ffebf17),
[Oura Skip](https://mobbin.com/screens/fb2b9bd2-c0a5-46d7-85f1-89cdc7b50a5c)).
Tvång här dödar räkmackan.

| Kan gå fel | Åtgärd |
|------------|--------|
| Klistrar betyg, klasslista, Unikum | Klientfilter + “det där sparar vi inte”. Strip. |
| Tror att skip = sämre sidekick | En rad: “Funkar utan. Du kan fylla i sen.” |
| För lång lapp | 280 tecken. Inte en uppsats. |

---

## S4 — invite (den sköra övergången)

| Kan gå fel | Åtgärd |
|------------|--------|
| iOS `requestChat` no-op | Visa “Lägg till i grupp” + länk. Inte en spinner som aldrig dör. |
| Botten inte admin | Gruppen skapas men invite failar. Text: “Gör botten till admin, en knapp.” |
| Befintlig familjegrupp med historik | Discord-heads-up: nya ser allt. **Tvinga ny tom grupp.** |
| Publik länk i klasschatten | `member_limit=3`, expire 48 h, ev. join-request. Föräldern godkänner. |
| QR mot barnet i köket | Ingen QR-knapp i förälderflödet. Bara share ([YouTube: share a link instead](https://mobbin.com/flows/65bc2203-0af3-409a-89b6-55064439b190)). |
| Barnet har inget Telegram | Säg det *här*, inte efteråt. Alt: 1:1 där föräldern vidarebefordrar. Inte PWA-ceremoni. |
| Föräldern “klar”-ar utan att dela | Inte klart. Primär knapp = Dela. Sekundär = Kopiera. |

[KOHO “unable to accept”](https://mobbin.com/screens/3ffdccc8-1c2f-4f87-bd48-f17173878465):
död länk behöver **Gå tillbaka + ny länk**, inte bara fel.

---

## S5 — väntar (ofta glömt)

| Kan gå fel | Åtgärd |
|------------|--------|
| 48 h går, tyst | Föräldern får ett meddelande i 1:1: “Länken dog. Ny?” |
| Syskon / kompis går med | Join-request. Botten svarar inte okända id. |
| Föräldern skriver i gruppen | Botten svarar bara barnets user_id. Förälder: “Du tittar. De skriver.” |
| Nudge | Inget “har de skrivit än?” mot barnet. Bara tyst panel till vuxen. |

---

## S6 — barnet skriver

Det är produktstart. Wizard ska vara osynlig. Om välkomsttexten
är “Vad vill du lära dig idag?” (nuvarande `WELCOME_MSG`) är det
läxgnäll. Byt till inget, eller en rad som en kompis.

---

## Det som redan är fel i koden (inte bara ritning)

1. `ALLOWED_CHAT_ID = 544123218` — räkmackan släpper inte in någon.
2. `/consent [lösenord]` — motsatsen till fyra tryck.
3. `/pause` lovas, saknas.
4. Samtyckestext och välkomst går till *samma* chatt. I gruppen
   måste de delas: vuxen ser samtycke, barn ser inte juristtext.
5. Mini App finns inte. `requestChat` kan inte verifieras här.

---

## Vad vi *inte* kan påstå efter den här miljön

- Att share-sheet känns bra på iPhone.
- Att iOS Mini App öppnas.
- Att createChatInviteLink landar i rätt grupp.
- Att barnet hittar gruppen bland 40 andra chattar.

Det testas på en riktig telefon, med en förälder som inte byggt
boten. `frontend/rakmacka.html` går att klicka: S0–S6 plus barn-
öppnade, lärare, iOS-fallback, bot-inte-admin och utgången länk.
Det är inte Telegram. Det är tillstånden.

---

## Krav innan P-39 räknas klar

- Back bevarar val (Markov).
- S3 skip lika stor som fortsätt.
- S4 inte “klart” förrän share eller copy.
- S5 synligt för föräldern.
- S0-barn blockeras.
- Ny länk vid expire ([KOHO](https://mobbin.com/screens/3ffdccc8-1c2f-4f87-bd48-f17173878465)).
- Ingen QR i förälderflödet.
- Ingen e-post på barnkortet.
