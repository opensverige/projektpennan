# Prenumerations-OAuth — Hermes-enkelt, inte förbjudet

Föräldern ska kunna trycka **Fortsätt med ChatGPT** och använda
det de redan betalar. Inte skapa ett API-konto. Inte klistra
`sk-` om de inte måste.

Mallen är Hermes Agent: en knapp, en länk, en kod, klar.
Inte en leverantörslista.

## Vad som är tillåtet

| Leverantör | Abonnemang → vår app | Hur |
|------------|----------------------|-----|
| **ChatGPT** | Ja, officiellt för Codex | `codex login` / device-sida `auth.openai.com/codex/device`. Hermes kör samma flöde. Plus eller högre. Device-kod kan behöva slås på under Säkerhet. |
| **Grok** | Ja, officiellt för Grok Build | `grok login` eller `--device-auth` (RFC 8628) mot `auth.x.ai`. SuperGrok / X Premium+. |
| **Claude** | **Nej** | Anthropic: OAuth för Free/Pro/Max är bara Claude.ai och Claude Code. Third-party som erbjuder “logga in med Claude” bryter villkoren. Nyckel eller Console-API. |

“Sign in with ChatGPT” hos Airtable/Notion är *identitet*, inte
modellen. Prenumerationen för *anrop* går via Codex-inloggningen.

Vi **låtsas inte** vara Codex eller Grok Build (inga fejkade
`x-grok-client-identifier`). Vi öppnar *deras* inloggning och kan
importera den lokala sessionen (`~/.codex/auth.json`,
`~/.grok/auth.json`) om den finns på datorn.

## Default-vägen

1. Vad heter barnet?
2. Jag är vårdnadshavare.
3. Fortsätt med ChatGPT **eller** Grok — öppnar *deras* inloggning.
4. Logga in hos dem. Tryck Jag är inne. Vi letar efter `~/.codex`,
   `~/.grok` eller Hermes `~/.hermes/auth.json`. Inga tokens i svaret.
5. Ingen session än? Stanna. Tryck igen, eller Fortsätt ändå.
6. Claude? Klistra nyckel. Ingen OAuth-knapp.

## Inte gjort

P-26: inloggningen anropar inte FastAPI-chatten än. Importen
säger bara om en lokal session *finns*. Tokens lämnar inte
webbläsaren som JSON i svaret.
