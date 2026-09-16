# Utter

[Svenska](README.md) · [English](README.en.md) · [Español](README.es.md) · [العربية](README.ar.md)

**A study companion for Swedish grades 4–6. The parent owns the plate. The child gets questions, not the answer.**

The child writes to **Utter**. The repository and initiative are **Projekt Pennan**, under [Open Sverige](https://opensverige.se). Licence: [AGPL-3.0](LICENSE).

This is a home tool. The school is never the operator. Lgr22 is an optional pack, not the boss. Extra support is the default. No homework nagging.

The **Swedish [README.md](README.md) is the source of truth.** This file is the short door for English readers. We do not keep four full manuals in sync.

---

## What the child gets

```
Child:  What is 7 times 8?
Utter: Do you know 7 × 7? Then we take one more step.
```

Never the answer first. Pace that fits. Stops when it gets hard. Visible to the parent.

We ship the **plate**: safety, consent, vault, pack format, logs.  
The parent jacks in a frontier model (ChatGPT, Grok, Claude key) or a capable open-source engine (Groq, vLLM). Ollama is a last resort, not the product. The plate stays when the brain changes.

---

## Run it locally (Open)

```bash
git clone https://github.com/opensverige/projektpennan
cd projektpennan
pip install -r backend/requirements.txt
export OPENAI_API_KEY=sk-...   # or XAI_ / ANTHROPIC_ / GROQ_
cd backend && uvicorn main:app --reload --host 127.0.0.1 --port 8080
```

[http://localhost:8080](http://localhost:8080) — child chat.  
[http://localhost:8080/guardian.html](http://localhost:8080/guardian.html) — thin log.

Without Docker: `pip install -r backend/requirements.txt`, then from `backend/`:  
`uvicorn main:app --reload --host 0.0.0.0 --port 8080`

Telegram is optional and **their** bot ([@BotFather](https://t.me/BotFather)). There is no official `@utter`. If we held the token we would see the chat in plaintext — we do not. On `main` a hardcoded allow-list chat id still exists (P-02). Do not run that bot for other families yet.

Hosted “Hem” (BankID, silent WhatsApp contact) is **not built**.

---

## Safety

The code decides. The model teaches.

- Crisis → a human. In Sweden: **BRIS 116 111**. No chatbot therapy. No follow-up question.
- Sex, violence, drugs → an adult at home, not the model.
- No secrets from the parent.
- Jailbreaks do not change the rules. The rules are not in the prompt.

If you host it (**Open**), we do not see the chats.  
If we host it (**Hem**), we would — DPIA first. Safety is never a paywall.

Full product, inventory, and backlog: [README.md](README.md).
