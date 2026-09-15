# Räkmackan — fyra tryck, sen en grupp

Arbetsnamn: Skooli Buddy. BankID är av. Vi är OSS. Vi har inte
den byråkratiska muskeln. Telegram *är* identiteten.

> Föräldern väljer agent, barn, kontext. Sen bjuder de in till
> en grupp. Barnet får ingen onboarding. Några knapptryck.

Det här är monumentet för setup. Inte Docker. Inte `/consent
[lösenord]`. Inte QR mot barnet.

## Vad föräldern måste ge (bara det)

| Steg | Fråga | Inte |
|------|-------|------|
| 1. Agent | Extra stöd / saga / tro / egen overlay | Modellnamn, API-nyckel |
| 2. Barn | Tilltalsnamn + åk | Efternamn, e-post, personnummer |
| 3. Kontext | Valfri lapp: “bråk, vikingar” eller hoppa över | Unikum-lösen, betyg |
| 4. Invite | Native share till Telegram-grupp | QR, ny app, “nu prata med AI:n” |

Samtycke är en checkbox på steg 1: “Jag är vårdnadshavare.”
Telegram-kontot som öppnade boten är föräldern. Inget BankID.
Inget lösen i chatten.

## Flödet (ritat, delvis byggt)

```
t.me/skoolibot?startapp
        │
        ▼
 Mini App / knapp-wizard   ← tre korta skärmar + chips
        │
        ▼
 “Skapa grupp”             ← Telegram native (requestChat / add-to-group)
        │
        ▼
 Invite-länk 48 h          ← createChatInviteLink, member_limit ~3
        │                    native share-sheet (WhatsApp/iMessage/Telegram)
        ▼
 Gruppen: förälder admin, bot svarar BARA barnet
 Barnet öppnar tråden när de kör fast. Inget gnäll.
```

Fallback om Mini App krånglar (iOS `requestChat` var stilla
trasig i maj 2026): vanliga knappar i 1:1 med boten, sen
“Lägg till i grupp” + länk.

## Vad som förbättrats i Telegram (2026)

Vi behöver inte uppfinna invite. Bot API har redan:

- **Mini Apps** — `t.me/bot?startapp`, setup inuti Telegram
  ([docs](https://core.telegram.org/bots/webapps))
- **Bot API 9.6 (april 2026)** — `requestChat` / prepared buttons:
  välj eller skapa grupp, lägg in botten som admin. Android funkar.
  iOS hade en känd no-op i maj — därför fallback.
- **`createChatInviteLink`** — namn, expire, member_limit,
  ev. join-request som föräldern godkänner
- Deep link `t.me/bot?start=TOKEN` — allowlist utan hårdkodat id (P-30)

Managed bots (`t.me/newbot/...`, två tryck till en ny bot) är
för *oss* som driftar, inte för barnet.

## UX vi lånar (produktion, inte moodboard)

Kort. Inte GoHenrys 16–24 skärmar.

| Lån | Var | Vad vi tar | Vad vi skippar |
|-----|-----|------------|----------------|
| [Customize ChatGPT](https://mobbin.com/flows/a3659710-c1a1-48b4-bbdb-505f969cb856) | 3 fält + chips | Agent-typ som chips, en kontext-ruta | “Vad jobbar du med?” |
| [ChatGPT group link](https://mobbin.com/flows/701c22ce-da6b-434f-8e8c-ac13b1a3e959) | Copy / Share | En länk, native share | Deras produkt dog juli 2026 — mönstret lever i Telegram |
| [Discord invite](https://mobbin.com/flows/203a63f2-c66e-49b4-bcce-7c6bf8879070) | 24 h-länk + heads-up | Expire + “bara de du bjuder” | 10-persons picker |
| [Greenlight send invite](https://mobbin.com/flows/98121fbb-0dab-4832-82f3-791d9f31321e) | Efter roll | Invite *efter* barnkort | SMS + efternamn + mobil |
| [YouTube Family](https://mobbin.com/flows/65bc2203-0af3-409a-89b6-55064439b190) | “Share a link instead” | Länk, inte QR mot barnet | Teen-e-post |

Anti-mönster: [GoHenry add a child](https://mobbin.com/flows/e6bbd01e-9404-45dc-94c5-aee3001372d7)
(e-post, ID-koll, 16 steg). Det är bank. Vi är en sidekick.

## Identitet utan BankID

| | Open / räkmacka | Senare, om någon betalar |
|---|-----------------|--------------------------|
| Förälder | Telegram-användaren som startade boten + checkbox | Ev. BankID som *tillval* för Hem-plus |
| Barn | Inget konto. Medlem i gruppen. | Samma |
| Allowlist | start-token + gruppens chat_id | Samma |

GDPR under 13: vårdnadshavares samtycke. Checkbox + att de
håller telefonen räcker för OSS-default. Hosted Hem som tar
betalt kan lägga BankID *senare*. Det är inte räkmackan.

## Inte i scopet för räkmackan

- Barn-onboarding, avatar, “vad vill du lära dig”
- Läx-nudge när gruppen är skapad
- QR som föräldern tvingar barnet att skanna i köket
- Skol-SSO
- Att *vi* skapar barnets Telegram-konto

## Status

Ritat. Inte byggt. Idag: `/consent [lösen]` + hårdkodat chat-id.
Nästa kod: P-39 (Mini App / knapp-wizard) + P-30 (token) + P-13
(grupp: bot svarar bara barnet).
