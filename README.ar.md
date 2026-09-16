<div dir="rtl" lang="ar">

# أوتر (Utter)

[Svenska](README.md) · [English](README.en.md) · [Español](README.es.md) · [العربية](README.ar.md)

**رفيق دراسة للصفوف ٤–٦ في السويد. وليّ الأمر يملك اللوحة. الطفل يأخذ أسئلة، لا الجواب.**

الطفل يكتب إلى **أوتر**. المستودع والمبادرة هما **Projekt Pennan** تحت [Open Sverige](https://opensverige.se). الرخصة: [AGPL-3.0](LICENSE).

هذه أداة بيت. المدرسة ليست المشغّل. منهج Lgr22 حزمة اختيارية، لا سيادة. الدعم الإضافي هو الافتراضي. لا إلحاح على الواجب.

**الحقيقة الكاملة بالسويدية:** [README.md](README.md). هذه بوابة قصيرة. لا نُشغّل أربع كتيّبات كاملة.

---

## ماذا يحصل عليه الطفل

```
الطفل:  كم ٧ في ٨؟
أوتر: هل تعرف ٧ × ٧؟ إذن نأخذ خطوة واحدة بعد ذلك.
```

أبدًا الجواب أولًا. إيقاع يناسب. يتوقف عندما يصعب. ظاهر لوليّ الأمر.

نحن نقدّم **اللوحة**: الأمان، الموافقة، الخزنة، الحزم، السجل.  
هم يركّبون نموذجًا حديثًا (ChatGPT أو Grok أو مفتاح Claude) أو محرّكًا مفتوحًا قويًا (Groq أو vLLM). Ollama ليس المنتج، بل آخر خيار.

---

## تشغيله محليًا (Open)

```bash
git clone https://github.com/opensverige/projektpennan
cd projektpennan
pip install -r backend/requirements.txt
export OPENAI_API_KEY=sk-...
cd backend && uvicorn main:app --reload --host 127.0.0.1 --port 8080
```

[http://localhost:8080](http://localhost:8080) — محادثة الطفل.  
[http://localhost:8080/guardian.html](http://localhost:8080/guardian.html) — سجل خفيف.

بدون Docker: `pip install -r backend/requirements.txt` ثم من `backend/`:  
`uvicorn main:app --reload --host 0.0.0.0 --port 8080`

تيليغرام اختياري و**بوتهم** ([@BotFather](https://t.me/BotFather)). لا يوجد `@utter` رسمي. لو عندنا الرمز لرأينا الدردشة نصًا واضحًا — لا نفعل. على `main` ما زال معرّف محادثة ثابت (P-02). لا تشغّله لعائلات أخرى بعد.

«Hem» (BankID، جهة واتساب صامتة) **غير مبنية**.

---

## الأمان

الشفرة تقرّر. النموذج يُعلّم.

- أزمة → إنسان. في السويد: **BRIS 116 111**.
- جنس، عنف، مخدرات → بالغ في البيت.
- لا أسرار عن وليّ الأمر.
- كسر القيود لا يبدّل القواعد. القواعد ليست في الـ prompt.

إن استضافوه (**Open**) لا نرى الدردشات.  
إن استضفناه نحن (**Hem**) نراها — أولًا تقييم أثر على الخصوصية. الأمان ليس خلف جدار دفع.

المنتج والجرد والباقي: [README.md](README.md).

</div>
