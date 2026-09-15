# UX-check — förälderstart

Gjort mot den vita wireframen. Betyget var B för att
**tre sidor talade tre språk**, inte för att flödet hade
för många steg.

## Vad som var fel

1. **Ingen designsystem.** Start var Grok-wireframe. Chatten
   var 2019-blå uggla. Föräldravy en tredje blå. En förälder
   tror att de hamnat i fel app.
2. **Inter laddades inte.** Systemstack. Ser ut som en
   placeholder.
3. **Native checkbox + fet/osynlig CTA.** Inget Field, ingen
   förklaring när pilen är grå.
4. **Placeholder-only.** “Vad heter barnet?” utan label —
   försvinner när de skriver, dåligt för a11y.
5. **Nyckel utan visa/dölj.** Hemlighet som man inte kan kolla.
6. **Chatten länkade förbi samtycke.** Och sa fortfarande
   “Skooli” när API dog.
7. **Av-rampen täckte fälten** (fixad) men såg ut som en gist,
   inte som produkten.

Flödet i sig var rätt: en skärm, klistra nyckel, päron gömda.
Vi bytte *hantverket*, inte wizard.

## Vad vi lånade

- **shadcn `login-03`** — Card + FieldGroup + Field + Input.
  Inte Apple/Google. Inte “Welcome back”.
- **shadcnblocks `login1`** — centrerad yta, muted canvas,
  ett kort, ett varumärke. Layouten. Inte e-post/lösen.
- **React Bits Aurora** — mjuk bakgrund, lightMode, dämpade
  jordfärger. Av om `prefers-reduced-motion`.
- Inte shadcnblocks `onboarding1` (fem steg, pro, dashboard-
  preview). Det är wizard igen.

## Check efter bytet

| Heuristik | Status |
|-----------|--------|
| En skärm, inga steg | OK |
| Klistra-fält är primära | OK, pil i InputGroup |
| Samtycke synligt, förklarat när det saknas | OK |
| Prefix viskar leverantör | Badge, inte dropdown |
| Päron bakom accordion | OK + toast vid kopiera |
| Samma tokens på start / chatt / föräldravy | OK |
| Touch ~44px på skicka | h-11 / h-12 |
| Label + visa nyckel | OK |
| Reduced motion | Aurora av |

## Medvetet inte

P-26 (nyckeln anropar inte FastAPI). Mörkt tema som default.
BankID. Barn-onboarding.
