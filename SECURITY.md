# Säkerhet

Skooli Buddy pratar med barn. Behandla varje rapport som om det
vore ditt eget barn i chatten.

## Rapportera
Maila maintainer via GitHub-säkerhetsadvisory på
[opensverige/projektpennan](https://github.com/opensverige/projektpennan)
eller öppna **inte** ett publikt issue för:

- sätt att kringgå samtycke, paus eller radering
- sätt att få ut raka svar / farligt innehåll
- läckage av loggar, chat-id, nycklar
- jailbreak som tar sig förbi koden (prompt-only räknas också)

## Vad som redan är känt
Se `docs/INVENTORY.md` och `docs/BACKLOG.md`. Bland annat:

- hårdkodat Telegram-id (P-02)
- safety.py täcker bara engelska (P-03)
- krisregel lever mest i prompten (P-03)
- dashboard läser fel loggfält (P-07)

Nya rapporter om just de punkterna: peka på backlog-id, öppna inte
dubbletter.

## Self-host
När du kör detta hemma är **du** personuppgiftsansvarig. Sätt
`GUARDIAN_PASSPHRASE`, släpp inte port 8080 mot internet, committa
aldrig `.env` eller `config/consents.json` med riktiga id.
