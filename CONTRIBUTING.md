# Bidra till Skooli Buddy

Tack. Det här är ett hemverktyg för barn. Vi tar PRs som om
föräldrar ska kunna läsa dem.

## Innan du kodar
1. Läs `docs/PRODUCT.md` — föräldern styr, skolan gör det inte.
2. Läs `docs/BACKLOG.md` och plocka ett ID (P-xx).
3. Ny pedagogik eller ny safety-regel? Skriv ett fynd först:

```bash
python scripts/research_pipeline.py new \
  --id kort-id --title "Påståendet" --theme pedagogy
python scripts/research_pipeline.py validate
```

## Grenar och tester
```bash
git checkout -b feat/kort-beskrivning
python -m pytest tests/ -v
python scripts/research_pipeline.py validate
python scripts/curriculum_cli.py validate
```

Persona-matrisen (`scripts/run_tests.py`) kräver Gemini-nyckel och
är inte ett krav för små PRs. Kör den om du rör `skooli_buddy/core.py`
eller tutor-reglerna.

## Vad vi inte mergar
- Skolintegrationer (Unikum, Classroom, kommun-SSO).
- Diagnosfält eller "NPF-läge" som stämplar barnet.
- Features som kräver att barndata lämnar hemmet utan tydlig opt-in.
- Prompt-only safety utan kod.
- Hemliga chat-id, nycklar eller riktiga barnprofiler.

## Regler
`agents/tutor/SOUL.md`, `SKILL.md`, `RULES.md` och
`SKOOLI_BUDDY_SAFETY_SPEC.md` är kontraktet. Duplicera dem inte i
Python. Om Yta A och Yta B divergerar: laga kärnan, inte README.

## Språk
Kodkommentarer och docs på svenska är ok. Barnets UI är alltid
svenska först. Commit-meddelanden: `typ: kort beskrivning`.
