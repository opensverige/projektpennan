# Är det här Hermes?

Kort: **form, inte runtime.**

[Hermes Agent](https://github.com/NousResearch/hermes-agent) är ett
filesystem-first agent-ramverk: `SOUL.md`, minne som filer, verktyg,
sessioner, cron. Vi lånade den formen.

| | Hermes | Gnista nu |
|---|--------|-----------|
| Identitet | `SOUL.md` på disk | `agents/tutor/SOUL.md` + SKILL + RULES |
| Minne | markdown-filer agenten läser/skriver | `vault/memory/` — samma idé, Obsidian-öppet |
| Hjärna | deras loop + verktyg | FastAPI + BYO (ChatGPT / Grok / Claude / Groq / vLLM) |
| Verktyg | terminal, web, cron | nej. Vi är en studiekompis, inte en datoroperatör |
| OAuth | deras device-flöde | vi öppnar *deras* Codex/Grok-sida, impersonerar inte |

Vi kör inte Hermes CLI. Vi är en **kernel med Hermes-formade filer**:
föräldern äger vaulten, byter modell, safety sitter i kod.

Obsidian: öppna mappen `vault/` som vault. `memory/barn.md`,
`intressen.md`, `gnistor.md` är vanliga notes med `[[wikilänkar]]`.
Ingen plugin, ingen moln-sync hos oss.
