# Utter

[Svenska](README.md) · [English](README.en.md) · [Español](README.es.md) · [العربية](README.ar.md)

**Un compañero de estudio para 4.º–6.º en Suecia. Quien cría posee la placa. El niño recibe preguntas, no la respuesta.**

El niño escribe a **Utter**. El repositorio y la iniciativa son **Projekt Pennan**, de [Open Sverige](https://opensverige.se). Licencia: [AGPL-3.0](LICENSE).

Es una herramienta del hogar. La escuela no es operadora. Lgr22 es un pack opcional, no la autoridad. El apoyo extra es el valor por defecto. Sin insistir con los deberes.

Quien cría la enciende y responde seis chips. El niño no ve ese formulario. La primera frase usa la puerta del intake. La cámara es un comienzo válido.

**La verdad del producto está en sueco:** [README.md](README.md). Este archivo es la puerta corta. No mantenemos cuatro manuales completos.

---

## Lo que recibe el niño

```
Niño:   foto av läxan
Utter: Alma. Redstone y las fracciones son lo mismo. ¿Qué hay de niebla en la foto?
```

Nunca la respuesta primero. Ritmo que encaja. Se detiene cuando duele. Visible para el padre o la madre. No es un panel del niño. No es un bucle tipo Shorts.

Nosotros damos la **placa**: seguridad, consentimiento, vault, packs, registro.
Ellos enchufan un modelo frontier (ChatGPT, Grok, clave de Claude) o un motor open-source capaz (Groq, vLLM). Ollama es el último recurso, no el producto.

---

## Arrancarlo en casa (Open)

```bash
git clone https://github.com/opensverige/projektpennan
cd projektpennan
pip install -r backend/requirements.txt
export OPENAI_API_KEY=sk-...
cd backend && uvicorn main:app --reload --host 127.0.0.1 --port 8080
```

[http://127.0.0.1:8080/start.html](http://127.0.0.1:8080/start.html) — nombre, clave, consentimiento.
Luego seis chips + saltar. Luego la vista previa. Luego el chat: primera frase + cámara.

Telegram es opcional y es **su** bot ([@BotFather](https://t.me/BotFather)). No hay un `@utter` oficial. Si nosotros tuviéramos el token, veríamos el chat en claro — no lo hacemos. En `main` sigue un chat-id fijo (P-02). No lo uses para otras familias todavía.

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
