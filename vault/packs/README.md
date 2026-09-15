# Packs — det föräldern äger

Kernel (safety, samtycke, runtime) är låst. Allt här är utbytbart.

En pack är en mapp med `manifest.json` plus markdown eller JSON.
Föräldern slår på, stänger av, skriver själv eller laddar upp.
Export = zip av `vault/`. Import på en annan maskin. Ingen molnplikt.

```
vault/packs/
  lgr22/            valfritt kursplanspack — default på i Sverige, av om föräldern vill
  worldview/        tro, värderingar, språk hemma
  pedagogy/         vilka metoder som får användas
  accommodations/   det föräldern valt att berätta (diagnos, preferenser)
  custom-agent/     egen SOUL/SKILL-overlay ovanpå kernel
  school-context/   vad som är uppe i skolan — förälder-ägt, minimerat
```

`manifest.json` måste följa `_schema/manifest.schema.json`.
`cannot_override_safety` är alltid true. En pack som ber om facit,
hemligheter från vårdnadshavare eller att stänga BRIS laddas inte.

Laddaren är backlog P-33. Tills den finns: policies.packs pekar på
vilka id som är tänkta att vara på; runtime läser ännu mest
`agents/tutor/` + `config/lgr22/` när curriculum-packen är satt.
