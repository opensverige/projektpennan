# Onboarding — avskalat, som Grok

Föräldern vi bygger åt är inte en developer. Förra
`start.html` var en install-wizard: sex steg, P-26-märken,
bas-URL, Docker mot Telegram. Det är Vibecode
([lista på ANTHROPIC_API_KEY](https://mobbin.com/screens/1d7d1e3a-0d6b-4f56-a2e9-5292cd3923f6)).
Inte Grok. Andra varvet var fortfarande ett *formulär*
(rubrik, två fält, fet knapp). Grok har ingen rubrik.

## Teamet

**Produkt (föräldern).** En tisdag. De har tre minuter. De ska
ge barnet en chatt, inte förstå en platta. Om de har en nyckel
ska de kunna klistra in den. Annars ska de ändå komma in.

**Grok-designern.** Efter konto är Grok en tom yta, ett
ordmärke och en pillerad
([Ask anything](https://mobbin.com/screens/f53f0654-607c-45e6-8533-1babfb09a1e3),
[How can I help](https://mobbin.com/screens/5a43c0f5-f1ea-4c20-a04c-e3d324bb912e)).
Pilen sitter *i* fältet. Deras *konto*-onboarding är 14
skärmar — den kopierar vi inte. Produkten är den tomma ytan.

**ChatGPT-designern.** Webben är en mening och en ruta
([What's on the agenda](https://mobbin.com/screens/d9925cb3-c483-46ed-8e7c-acfdf39185b9),
[Ready to dive in](https://mobbin.com/screens/9b4ff6b8-cf1c-4344-92c5-15bcff3e226b)).
Ingen leverantörsväljare. Ingen signup-knapp under.

**Secrets-designern.** Ett fält, “klistra in här”. Inte
OpenAI Platform / Relevance AI med region och curl
([Grok-nyckel + curl](https://mobbin.com/screens/5fe0f0c1-56f6-4d67-942f-604073ce4c72)
är päron-sidan, inte förstasidan). WhatsApp hemlig kod: ett
fält, en mening
([skärm](https://mobbin.com/screens/f43918a2-fbc9-424f-91a3-fbe214344f91)).

**Päron-off-ramp.** Den som vill ha ChatGPT-integration eller
Docker får en *prompt att klistra* och en rad, gömd bakom
“Bygger du själv?”. Inte på förstasidan.

## Default-vägen (en skärm, som produkten)

Ordmärke. Namn som en tyst rad. Sen *ett* pastafält.

1. Vad heter barnet?
2. Klistra in nyckeln här. (valfritt)
3. Jag är vårdnadshavare.
4. Pilen i fältet.

Nyckelns prefix avgör leverantören tyst (`sk-`, `sk-ant-`,
`AIza`, `xai-`). En viskning “Det där ser ut som ChatGPT”
är allt de ser. Aldrig “openai-compat”.

Ingen progress-bar. Ingen fet “Sätt igång”. Inget recept i JSON.

## Av-ramp

Bakom en textlänk längst ner: kopiera en systemprompt till
ChatGPT, eller en rad Docker. Det är för päronen. Det är
inte onboardingen.

## Inte Grok-konto

Vi kopierar inte e-post + kod + lösen. Vi har inget konto.
Telegram-identitet och ev. Hem kommer sen. Den här skärmen
ska kännas som *produkten*, inte som signup.
