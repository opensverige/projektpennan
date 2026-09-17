# Research pipeline

Research är inte en moodboard. Det är hur vi bestämmer vad som får
ändra pedagogik, safety och föräldrakontroll.

```
källa i sources.json
        │
        ▼
  finding (JSON, ett påstående)
        │
        ├─ validate  → schema + kända källor
        ├─ summary   → lägesbild per tema
        └─ backlog   → produktimplikationer kopplade till docs/BACKLOG.md
```

## Kommandon

```bash
python scripts/research_pipeline.py sources    # katalog
python scripts/research_pipeline.py list       # alla fynd
python scripts/research_pipeline.py validate   # CI-steg
python scripts/research_pipeline.py summary    # per tema
python scripts/research_pipeline.py backlog    # implikationer
python scripts/research_pipeline.py new \
  --id kort-id --title "Rubrik" --theme pedagogy
```

Inget nätverksanrop. Vi hämtar inte papper automatiskt — vi skriver
fynd för hand så att en människa har läst källan.

SKU-gräns för intag (fil vs Hem vs Kväll): [docs/INTAKE.md](../docs/INTAKE.md),
fynd `intake-not-file`.

## När ska ett fynd in?
- Ny evidens för en lärandeform vi använder eller skippar.
- Ny IMY / Skolverket / SPSM-vägledning.
- Konkurrent som sätter en ribba för föräldrakontroll.
- Utvärdering från våra egna tester eller barntest.

## Teman
`pedagogy` `safety` `privacy` `product` `curriculum` `accessibility`

## Status
`draft` (påståendet är fångat) → `accepted` (får styra backlog) →
`superseded` (ersatt av nytt fynd).

## Regel
Ett fynd = **ett påstående**. Inte en länkdump. Implikationen ska
kunna bli en rad i `docs/BACKLOG.md`.
