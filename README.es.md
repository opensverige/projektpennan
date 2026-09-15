# Gnista

[Svenska](README.md) · [English](README.en.md) · [Español](README.es.md) · [العربية](README.ar.md)

**Un compañero de estudio para 4.º–6.º en Suecia. Quien cría posee la placa. El niño recibe preguntas, no la respuesta.**

El niño escribe a **Gnista**. El repositorio y la iniciativa son **Projekt Pennan**, de [Open Sverige](https://opensverige.se). Licencia: [AGPL-3.0](LICENSE).

Es una herramienta del hogar. La escuela no es operadora. Lgr22 es un pack opcional, no la autoridad. El apoyo extra es el valor por defecto. Sin insistir con los deberes.

**La verdad del producto está en sueco:** [README.md](README.md). Este archivo es la puerta corta. No mantenemos cuatro manuales completos.

---

## Lo que recibe el niño

```
Niño:   ¿Cuánto es 7 por 8?
Gnista: ¿Sabes cuánto es 7 × 7? Entonces damos un paso más.
```

Nunca la respuesta primero. Ritmo que encaja. Se detiene cuando duele. Visible para el padre o la madre.

Nosotros damos la **placa**: seguridad, consentimiento, vault, packs, registro.  
Ellos enchufan el modelo: Ollama en casa, o ChatGPT / Grok / su propia clave. La placa sigue cuando el cerebro cambia.

---

## Arrancarlo en casa (Open)

Sin LLM en la nube. Los datos se quedan en `vault/`.

```bash
git clone https://github.com/opensverige/projektpennan
cd projektpennan
# Ollama, p. ej. hermes3:8b en 11434
docker compose up --build
```

[http://localhost:8080](http://localhost:8080) — chat del niño.  
[http://localhost:8080/guardian.html](http://localhost:8080/guardian.html) — registro fino.

Sin Docker: `pip install -r backend/requirements.txt`, desde `backend/`:  
`uvicorn main:app --reload --host 0.0.0.0 --port 8080`

Telegram es opcional y es **su** bot ([@BotFather](https://t.me/BotFather)). No hay un `@gnista` oficial. Si nosotros tuviéramos el token, veríamos el chat en claro — no lo hacemos. En `main` sigue un chat-id fijo (P-02). No lo uses para otras familias todavía.

“Hem” (BankID, contacto silencioso en WhatsApp) **no está construido**.

---

## Seguridad

El código decide. El modelo enseña.

- Crisis → una persona. En Suecia: **BRIS 116 111**.
- Sexo, violencia, drogas → un adulto en casa.
- Sin secretos frente a quien cría.
- Un jailbreak no cambia las reglas. No viven en el prompt.

Si lo alojan ellos (**Open**), no vemos los chats.  
Si lo alojamos nosotros (**Hem**), sí — primero un DPIA. La seguridad no se cobra.

Producto, inventario y backlog: [README.md](README.md).
