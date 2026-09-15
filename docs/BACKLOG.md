# Backlog — det som återstår

Prioritet: P0 blockerar ärlig OSS-release. P1 gör produkten till
en sidekick föräldrar kan lita på. P2 är bredd. Varje post ska
kunna bli ett GitHub-issue. Research-id pekar på `research/findings/`.

## P0 — går inte att släppa öppet utan det här

| ID | Vad | Varför | Research |
|----|-----|--------|----------|
| P-01 | **En kärna, två ytor.** SOUL/SKILL/RULES + safety + logg + profil som enda sanning. `core.py` slutar äga en egen prompt. | Dubbel stack + motstridig AI-identitet. | `inventory-dual-stack` |
| P-02 | **Ta bort hårdkodat `ALLOWED_CHAT_ID`.** Allowlist via start-länk / env. Tom = vägra starta. | Privat id läckte. Andra kunde inte köra. Se `skooli_buddy/telegram_link.py`. | |
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

## P3 — produktifiering (kernel / Hem / Auto)

Se `docs/PRODUCTIZATION.md` och `docs/PRICING.md`. Inte sälj innan
P-03 och P-29.

| ID | Vad | Varför | Research |
|----|-----|--------|----------|
| P-25 | **Kernel-gräns i repo.** Hosted = tenant + identitet + faktura, inte en fork av pedagogiken. | Accounted-modellen. | `accounted-open-core` |
| P-26 | **Provider-adapter.** Läser `vault/config/runtime.json`. Ollama / OpenAI / Anthropic / Gemini / OpenAI-compat. BYO-nyckel i env. | Föräldern jackar in frontier-modeller. Plattan består. | `parent-baseplate` |
| P-27 | **Förälder-PWA** (BankID, PIN, paus). Barn-PWA bara fallback. | Förälderns yta ≠ barnets yta. | `contact-not-destination` |
| P-28 | **Webb-först onboarding.** En skärm: namn, klistra nyckel, samtycke. BankID bara på Hem sen. | Börjar i webben, inte Docker. Se `frontend/start.html`. | `parent-baseplate` |
| P-29 | **DPIA + underbiträden + ZDR** innan första betalande familj. | Hosted = vi är personuppgiftsansvariga. | `gdpr-hem` |
| P-30 | **Telegram start-token + allowlist** (dödar hårdkodat id). | Open och Hem. | `channel-sweden` |
| P-31 | **Publik prissida + DPA-text** (Open / Hem / egen drift). | Accounted-tabell. Aldrig paywalla safety. | `accounted-open-core` |
| P-32 | **WhatsApp som Hem-barn-default:** tyst kontakt, bild, röst. Inget läxpush. | Där de redan är. | `contact-not-destination` |

## P4 — förälderns kernel (packs, inte överhet)

Se `docs/PLATFORM.md`. Arbetsnamn. Lgr22 är pack. Safety är kernel.

| ID | Vad | Varför | Research |
|----|-----|--------|----------|
| P-33 | **Pack-laddare + egen agent.** Läs `vault/packs/*/manifest.json`. Upload av markdown-overlay. Konflikt mot safety = pack vinner inte. Export/import av vault-zip. | Föräldern ska inte sitta i vendor lock-in. Kernel, inte en låst app. | `parent-sovereignty-kernel` |
| P-34 | **Världsbilds-pack.** Föräldern slår på tro/värderingar i lärandet. Neutral bara när packen är av. Barnet kan inte byta pack. | Föräldern — inte läroplanen — styr livsåskådning. | `parent-sovereignty-kernel` |
| P-35 | **Pedagogikbibliotek i kod.** Sokrates, små steg, worked, CPA, saga, lek, retrieve, lässtöd. Byt metod när det kärvar. `nudge_homework=false`. | En metod räcker inte. Intresse utan gnäll. | `pedagogy-beyond-socratic` |
| P-36 | **Förälder-skrivna anpassningar.** Valfritt fält för diagnos/preferenser. Tyst anpassning. Krypterat i Hem. Aldrig till skola. Tomt = extra-stöd-default. | Vi sätter inte diagnos. Vi lyssnar när hemmet berättar. Art. 9. | `parent-authored-accommodations` |
| P-37 | **Skolkontext-pack.** Föräldern skriver veckans teman eller släpper in ICS/export. Minimering + TTL 7–14 dagar. Relevans i chatten, inget läxlarm. | Sidekicken ska veta vad som är uppe, utan att suga i sig Unikum. | `parent-owned-school-context` |
| P-38 | **Förälder-hostad connector.** De kör den hemma med sitt BankID/lösen. Skriver minimerad `context.json` till vault. Hem får aldrig skol-credentials eller live-API. | Byggarföräldrar gör det redan. Vi standardiserar formatet, inte inloggningen. | `parent-owned-school-context` |
| P-40 | **Byt arbetsnamn → Gnista.** Kontakt i chatt, bot, frontend, safety-spec. Projekt Pennan stannar. Stjärnis bara som valfritt pack. | Skooli Buddy krockar med Homework Buddy / Studybuddy. Se `docs/NAME.md`. | `product-name` |
| P-41 | **Förälder-start: en skärm.** Namn + klistra nyckel. Grok-tom, inte wizard. Av-ramp för päron. | Föräldern är inte developer. Se `docs/ONBOARDING.md`. | `parent-baseplate` |
| P-42 | **Prenumerations-OAuth.** ChatGPT + Grok via device-länk (Hermes/Codex/Grok Build). Claude förbjuden. Lokal import av `~/.codex` / `~/.grok`. Inte impersonation. | Föräldern har redan betalat. Se `docs/OAUTH.md`. | `oauth-subscription` |
| P-43 | **Förälder-testmiljö.** Plan + scenario-chips (även opassande) innan barnet släpps in. Samma safety-kärna. Igenkännbara ChatGPT/Claude/Grok-märken. | Föräldern ska känna sig säker. Se `frontend/test.html`. | `parent-preview` |
| P-44 | **Kärndemo utan Ollama.** `scripts/demo.sh` + `backend/demo.py`. Chatten faller tillbaka till kärnan. | Kunna testa i kväll. Inte låtsas att Grok svarar. | |

## Medvetet inte i scopet
- Skola som operatör: Unikum-SSO, klass-tenant, lärarvy, write-back.
- Officiellt partnerskap där *vi* loggar in mot kommunens plattform.
- Att suga i oss betyg, klasslistor eller hela veckobrev.
- Betyg, NP-förberedelse som facit-motor.
- Reklam, trackers, tillväxt-hack mot barn.
- Diagnosverktyg.

## Förslag på närmaste PR:er
1. P-02 + P-30 + P-07 — allowlist, start-token, dashboard, `/pause`.
2. P-03 — safety i kod, BRIS utan LLM.
3. P-01 + P-26 — en kärna, BYO-providers.
4. P-32 — WhatsApp-kontakt som barnets yta (då först Hem-känsla).
5. P-27 — förälder-PWA vid sidan av, inte som barnets destination.
6. P-29 — DPIA innan någon faktura (Meta i underbiträdeslistan).
7. P-33 + P-34 — pack-laddare och världsbild (då först kernel-känsla).
8. P-35 + P-36 — metodbyte i kod + krypterade anpassningar.
9. P-37 — veckans lapp (då först relevant utan läcka). P-38 sen.
