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

## Vad importen gör

`POST /api/oauth/import/{provider}` läser token från den lokala
filen, skriver `vault/config/oauth-session.json` (0600) och
svarar `{ok, provider, source, ready}` — aldrig token.
`providers.load_runtime` använder den om föräldern valt
ChatGPT/Grok och ingen `sk-` finns. Samma nyckel går till
webben och Telegram via `run_pipeline`.
