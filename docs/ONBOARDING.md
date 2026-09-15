# Onboarding — avskalat, som Grok

Föräldern vi bygger åt är inte en developer. Förra
`start.html` var en install-wizard: sex steg, P-26-märken,
bas-URL, Docker mot Telegram. Det är Vibecode
([lista på ANTHROPIC_API_KEY](https://mobbin.com/screens/1d7d1e3a-0d6b-4f56-a2e9-5292cd3923f6)).
Inte Grok.

## Teamet

**Produkt (föräldern).** En tisdag. De har tre minuter. De ska
ge barnet en chatt, inte förstå en platta. Om de har en nyckel
ska de kunna klistra in den. Annars ska de ändå komma in.

**Grok-designern.** Efter konto är Grok en tom yta och
“Ask anything”
([chatt](https://mobbin.com/flows/5ceeca79-6456-46c8-a95c-d113294f0fa9),
[hem](https://mobbin.com/flows/4d069838-3109-4241-9086-405c81b309f1)).
Deras *konto*-onboarding är 14 skärmar — den kopierar vi inte.
Produkten är den tomma ytan.

**ChatGPT-designern.** Webben är en mening och en ruta
([Ready when you are](https://mobbin.com/screens/18548847-534b-4263-9ffb-3f6cfdda7582),
[Where should we begin?](https://mobbin.com/screens/89314f68-aeb4-4303-b4d2-e36e9ff43cd6)).
Ingen leverantörsväljare.

**Secrets-designern.** Brave livestream: ett fält, “Enter your
key here”, en knapp
([skärm](https://mobbin.com/screens/47ad645e-8764-4950-b76a-f256854326e7)).
WhatsApp hemlig kod: ett fält, en mening
([skärm](https://mobbin.com/screens/39a7a3d6-80ac-44e8-9b2b-a951a2791c4d)).
Inget RPC-URL. Inget modellnamn.

**Päron-off-ramp.** Den som vill ha ChatGPT-integration eller
Docker får en *prompt att klistra* och en länk, gömd bakom
“Bygger du själv?”. Inte på förstasidan.

## Default-vägen (en skärm)

1. Jag är vårdnadshavare.
2. Vad heter barnet?
3. Klistra in nyckeln här. (valfritt)
4. Sätt igång.

Nyckelns prefix avgör leverantören tyst (`sk-`, `sk-ant-`,
`AIza`, `xai-`). Föräldern ser aldrig “openai-compat”.

Ingen progress-bar. Inget recept i JSON. Inget “kör i kväll”.

## Av-ramp

Bakom en textlänk: kopiera en systemprompt till ChatGPT, eller
en rad Docker. Det är för päronen. Det är inte onboardingen.

## Inte Grok-konto

Vi kopierar inte e-post + kod + lösen. Vi har inget konto.
Telegram-identitet och ev. Hem kommer sen. Den här skärmen
ska kännas som *produkten*, inte som signup.
