# Backlog — det som återstår

Prioritet: P0 blockerar ärlig OSS-release. P1 gör produkten till
en sidekick föräldrar kan lita på. P2 är bredd. Varje post ska
kunna bli ett GitHub-issue. Research-id pekar på `research/findings/`.

## P0 — går inte att släppa öppet utan det här

| ID | Vad | Varför | Research |
|----|-----|--------|----------|
| P-01 | **En kärna, två ytor.** SOUL/SKILL/RULES + safety + logg + profil som enda sanning. `core.py` slutar äga en egen prompt. | Dubbel stack + motstridig AI-identitet. | `inventory-dual-stack` |
| P-02 | **Ta bort hårdkodat `ALLOWED_CHAT_ID`.** Allowlist via env/`config`, default tom = vägra starta. | Annars läcker ett privat Telegram-id och boten är oanvändbar för andra. | |
| P-03 | **Safety i kod på båda ytorna.** Svenska+engelska mönster, kris → BRIS-svar utan LLM, jailbreak-filter. | Prompt räcker inte. `safety.py` är engelska-only. | `safety-code-not-prompt` |
| P-04 | **CI:** pytest, `research_pipeline.py validate`, `curriculum_cli.py validate`. `pytest` i requirements. | OSS utan grön pipeline är teater. | |
| P-05 | **README som stämmer.** En story: lokal default, Telegram valfritt, länka inventory/backlog/research. | README sålde bara Gemini. AGENTS sålde bara Ollama. | |
| P-06 | **Inga hemligheter i git.** Audit-secret-generering ok, men dokumentera. Rotera exempel. | Föräldrar som forkar ska inte ärva vårt id. | |
| P-07 | **Fixa dashboard-fält** `user_text`/`bot_text`. Implementera `/pause`. | Vi lovar insyn och paus i samtyckestexten. | `parent-controls` |

## P1 — föräldern i spakarna + extra stöd

| ID | Vad | Varför | Research |
|----|-----|--------|----------|
| P-08 | **Föräldrapanel som styr**, inte bara tittar. Samtycke, paus, tid, bilder, stödläge, export, radera. Lösenord + rate-limit. | Sorin/Tutur/Latio vinner på kontroll. Vi ska vinna på öppen kontroll. | `parent-controls` |
| P-09 | **Stödlägen i profil:** sokratisk / små_steg / kviss / läs_stöd. Föräldern sätter. Koden väljer SKILL-förmåga. | Extra stöd är vårt jobb, inte en prompt-rad. | `udl-extra-stod`, `literacy-split` |
| P-10 | **Persisterat minne (lokalt):** var vi slutade, vad som funkade, vad som kärvade. Inga diagnoser. Föräldern kan nolla. | Roadmap v0.4. Utan minne är varje kväll dag ett. | `socratic-ai` |
| P-11 | **Lgr22 åk 4–6** i `config/lgr22/` + spegling till vault för RAG. CLI: validate, add, diff mot källa. | 13 poster räcker inte för en studiekompis. | `lgr22-coverage` |
| P-12 | **Bild på läxan** (opt-in). Ingen ansiktslagring. Pedagogiska bilder ut. | Roadmap v0.3. Tutur vinner på kamera. | `parent-controls` |
| P-13 | **Telegram-grupp:** förälder spectator, barnet pratar, boten svarar bara barnet. | Roadmap v0.2. Insyn i realtid utan att störa. | `parent-controls` |
| P-14 | **Kris + extra stöd-personor i CI** (Leo, Nour, "orkar inte", lång text). Deterministiska tester där det går, Gemini-eval nattetid. | Ett barntest är anekdot. | `socratic-ai`, `literacy-split` |
| P-15 | **Lokal modell som förstaval.** Ollama-adapter bakom samma `get_response`. Gemini bakom flagga. | Integritet + OSS-trovärdighet. Gemini-ToS ändras. | `gdpr-hem` |

## P2 — grym produkt, inte bara korrekt

| ID | Vad |
|----|-----|
| P-16 | Röst in/ut (talsyntes + tal-till-text) som *tillval* för läs/skrivsvårigheter. Separera från kunskapsinhämtning. |
| P-17 | Matematisk verifiering (sympy/egna regler) så boten inte "firar" fel svar. |
| P-18 | Åk 1–3 och 7–9. Flera barnprofiler i samma hem. |
| P-19 | WhatsApp-adapter bakom samma kärna. |
| P-20 | Veckosammanfattning till föräldern: ämnen, ork, genombrott, förslag på analog hjälp — aldrig betyg. |
| P-21 | Arkivering/rotation av `logs/`, `vault/conversations/`, `vault/audit/`. |
| P-22 | CODE_OF_CONDUCT, issue-mallar, översättning av docs till engelska *utan* att byta barnspråk. |
| P-23 | Threat model: prompt injection via läxbild, syskon som gissar lösenord, läckta JSONL. |
| P-24 | Utvärdering mot riktiga familjer (samtycke, etikprövning-känsla även om det inte är forskning): NPF, SVA, "jag hatar matte". |

## Medvetet inte i scopet
- Integration mot Unikum, InfoMentor, Google Classroom, Skolon.
- Lärar-dashboard eller klasslista.
- Betyg, NP-förberedelse som facit-motor.
- Reklam, trackers, tillväxt-hack mot barn.
- Diagnosverktyg.

## Förslag på närmaste tre PR:er efter den här
1. P-02 + P-07 (allowlist + dashboard + `/pause`) — liten, synlig.
2. P-03 (gemensam `safety`-modul, svenska mönster, BRIS utan LLM).
3. P-01 start: `core.py` läser SOUL/SKILL/RULES istället för att
   äga en kopia.
