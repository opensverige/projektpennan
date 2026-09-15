# Installera — räkmacka vs kvällens Open

Arbetsnamn: Skooli Buddy. Kernel föräldern äger.
**BankID är av i default.** Vi är OSS.

| | **Idag (byggt)** | **Räkmackan (monumentet, ej byggt)** |
|---|------------------|--------------------------------------|
| Vem | Vi, tech-förälder | Vanlig förälder, några tryck |
| Barn ser | 1:1-bot eller localhost:8080 | En Telegram-grupp de redan kan |
| Förälder gör | Klona, `.env`, `/consent [lösen]` | Agent → barn → kontext → bjud in |
| Identitet | Lösenord i chatten | Telegram-kontot + checkbox |
| Onboarding | Nej. Kommandon. | Ja — P-39. Inte byggt. |
| Barn-onboarding | Avsiktligt ingen | Avsiktligt ingen |

Detalj: [docs/RAKMACKA.md](RAKMACKA.md).

---

## Scenariot vi håller uppe (räkmackan)

Söndag. Barnen är i sitt rum. Föräldern öppnar
`t.me/skoolibot?startapp` på *sin* telefon.

1. **Agent** — Extra stöd / saga / tro / egen. Chips. En checkbox:
   jag är vårdnadshavare.
2. **Barn** — Tilltalsnamn + åk. Inte efternamn. Inte e-post.
3. **Kontext** — “Den här veckan: bråk.” Eller hoppa över.
4. **Invite** — Skapa grupp. Native share. Länken dör på 48 timmar.

Barnet får en grupp i listan, mellan Mamma och Omar.
Ingen demo. Ingen QR. Första gången de skriver är första gången
produkten börjar.

---

## Scenariot som går att köra i kväll (Open)

### A. Lokal kernel

```bash
git clone https://github.com/opensverige/projektpennan
cd projektpennan
docker compose up --build   # Ollama på 11434
# http://localhost:8080
```

### B. Telegram som den ser ut nu

```bash
pip install -r requirements.txt
cp .env.example .env
python -m skooli_buddy.bot
```

`/consent [lösenord]` → `/start`. Hårdkodat chat-id (P-02).
Det är inte räkmackan.

---

## Vad som medvetet inte krävs

- BankID
- Barnkonto
- QR
- Unikum
- Att föräldern kan Docker (det är Open, inte räkmackan)
