# UX-scenarier — vi är där barnet redan är

> Inte: "Kolla här. Nu ska du prata med den här."
> Utan: en kontakt i chattlistan, mellan Mamma och Omar.
> Barnet öppnar den självmant. Som en kompis.

QR-kod + ny flik + "sitt och prata med AI:n" är en vuxenritual.
Barnet har redan mobilen. De scrollar, leker, skickar bilder,
pratar med kompisar. Vi ska inte ta dem därifrån. Vi ska finnas
*i samma gest*.

## Anti-scenariot (så gör vi inte)

Tisdag 19:10. Föräldern kommer in.

"Lägg undan luren. Skanna den här. Nu ska du göra matte med Skooli."

Barnet öppnar en främmande webbsida. Det känns som extra läxa.
De gör tre turer för att bli klara. Imorgon öppnar de den aldrig igen.

Det är Duolingo-stund. Det är inte en sidekick.

## Scenariot vi bygger

### 0. Föräldern sätter upp — barnet är inte i rummet

Söndag kväll. Barnen sover eller sitter i sitt rum.
Föräldern tar BankID på *sin* telefon, kryssar samtycke, sätter
tid, stödläge och ev. världsbild. Sen gör de samma sak som när mormor skulle
in i barnets WhatsApp: **lägger till en kontakt.**

Skooli dyker upp i barnets chattlista. Inget tal. Ingen demo.
Kanske en enda mening i familjechatten: "Skooli ligger i dina
chattar om du kör fast." Sen släpper de det.

Förälderns yta är en tyst panel: igång / pausa / tid. Inte en
scen att sätta barnet framför.

### 1. Barnet kör fast — själva

Tisdag 19:14. Sängen eller soffan. Snapchat är öppen i bakgrunden.
Matteboken ligger bredvid. De har redan fotat talet (det gör de
ändå, för att visa en kompis eller spara).

De gör det de alltid gör: öppnar WhatsApp. Skooli sitter där
som vem som helst. De trycker på tråden. Skickar bilden.
Skriver "fattar inte".

Det är samma motorik som [skicka en bild till en kompis](https://mobbin.com/flows/d7c12641-fbf6-4c95-ad93-e020a53bee9c):
kamera eller rulle → caption → skicka. Inte "öppna läxappen".

Skooli svarar som en kompis, inte som en lektion:

"Oj, det där pluset. Vad är det första du skulle räkna ut?"

Inget "bra fråga!". Ingen startskärm. Ingen onboarding för barnet.

### 2. De är bara nyfikna

Lördag. De scrollar. Plötsligt: "varför är blod rött?"
De skriver till Skooli som de skulle skrivit till en storebror.
Vi tar emot det. Vi är inte bara läxläge.

Om de skickar memes eller "hej" — svara kort, mänskligt, släpp.
Tvinga inte in matte. Sidekick som *bara finns* när de vill.

### 3. Röst, för de orkar inte skriva

De håller inne mikrofonen. Som till kompisen.
[Samma WhatsApp-tråd, samma mic](https://mobbin.com/screens/ae24c300-4896-4223-9285-ad0be9cb182d).
Vi skriver tillbaka kort. (Röst ut är senare. In räknas redan.)

### 4. Föräldern syns inte i barnets flöde

Inget "mamma tittar nu". Inget läxalarm från oss.
Om taket är nått: en vänlig stängning i *samma chatt*, inte en
förälder som kommer in med luren.

Föräldern får en tyst sammanfattning på *sin* telefon, bakom PIN.
Insyn, inte övervakningsshow i barnets ansikte.

### 5. De slutar — själva

De byter till Roblox. Chatten ligger kvar.
Nästa gång de kör fast vet de var den är.
Vi naggar inte. Vi pushar inte "dags för åtta minuter matte".

## Vad "där barnet är" betyder i praktiken

| De gör redan | Vi hakar i | Vi bygger inte |
|--------------|------------|----------------|
| WhatsApp med mamma / kompisar | Skooli som kontakt i samma app | En ny app att "öppna för läxan" |
| Fota talet, skicka till kompis | Samma bild, samma plus-knapp, annan tråd | QR till en web-chat |
| Voice note | Samma mic | Tvinga text |
| Familjegrupp | Skooli *kan* sitta där, men svarar bara när barnet adresserar — annars 1:1 | Bota som avbryter middagssnacket |
| Snapchat, TikTok, Roblox | Vi kan inte bo där (inga seriösa API:er för barn-tutor) | Låtsas att vi är en Roblox-mod |

PWA och QR är **förälderns fallback** (ingen WhatsApp, max integritet,
gemensam iPad). De är inte barnets vardagsväg.

Telegram är Open / nördförälder. Inte Hem-berättelsen.

## Produktregler som följer av scenariot

1. **Kontakt, inte destination.** Barnet ska aldrig "gå till Skooli".
   De ska skriva till Skooli.
2. **Noll barn-onboarding.** Inget "välj avatar", inget "vad vill du
   lära dig idag?"-start. Första meddelandet *är* starten.
3. **Inget läxpush.** Föräldern får inte ett "påminn barnet"-verktyg
   som startar en session. Det dödar självmant.
4. **Samma chattgester.** Bild, röst, klistermärken, korta meningar.
   UI:t är WhatsApps, inte vårt.
5. **Namn som en kompis.** "Skooli", inte "Skooli Buddy Läxhjälp AI".
6. **En tyst add.** Föräldern lägger in kontakten som mormor.
   Inte en ceremoni med barnet i knät.

## Vad som måste bli sant i koden

- Hem-default-yta: **WhatsApp-kontakt** (P-32 upp i prioritet),
  inte barn-PWA.
- Första meddelandet från barnet aktiverar, inte `/start` som
  föräldern tvingar dem att skriva.
- Bild och röst i den ytan tidigt — det är hur de redan pratar
  ([WhatsApp kamera/rulle](https://mobbin.com/flows/ca93b7e8-0110-49f4-9b62-8ae5c6794a0f)).
- Föräldrapanel på *förälderns* telefon. Aldrig som overlay
  på barnets chatt.
- Inga "tid att plugga"-notiser till barnet.

Meta som underbiträde är priset för att vara där de är. Det ska
stå i samtycket, ärligt. Den som vägrar Meta kör Open + lokal
PWA — utan att vi låtsas att det är samma vardagsväg.
