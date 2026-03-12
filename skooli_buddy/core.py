"""
Hjärnan i Skooli Buddy.
Bygger systemprompt, hanterar konversationshistorik och anropar Gemini 2.5 Flash.
"""
import os
import sys
import json
from typing import Any

import google.generativeai as genai
from google.generativeai.types import HarmCategory, HarmBlockThreshold
from dotenv import load_dotenv

from .profile import load_profile

load_dotenv()

# Konversationshistorik per chat_id: {chat_id: [{"role": ..., "parts": [...]}]}
_histories: dict[int, list[dict[str, Any]]] = {}
_MAX_TURNS = 20

# Gemini-modell och systemprompt initieras vid import
_model: genai.GenerativeModel | None = None


def _build_system_prompt(profile: dict) -> str:
    """Bygger systemprompt med barnets profil och Lgr22-kontext."""
    child = profile["child"].get("child", profile["child"])
    policies = profile["policies"]

    # Hämta child-data med fallbacks
    child_name = child.get("display_name", "Eleven")
    child_age = child.get("age", 10)
    child_grade = f"åk {child.get('grade', 4)}"
    child_grade_num = child.get("grade", 4)
    child_interests = ", ".join(child.get("interests", []))
    child_strengths = ", ".join(child.get("subjects", []))
    child_development_areas = "problemlösning och kritiskt tänkande"

    # Bygg curriculumkontext
    curriculum_lines = []
    for entry in profile["curriculum"]:
        curriculum_lines.append(
            f"- [{entry.get('subject', '')} åk{entry.get('grade', '')}] "
            f"{entry['area']}: {entry['content'][:120]}"
        )
    curriculum_context = "\n".join(curriculum_lines) if curriculum_lines else "Lgr22 allmän kursplan"

    # Bygg policies-kontext
    pedagogy = policies.get("pedagogy", {})
    policies_context = (
        f"Sokratiskt läge: {'på' if pedagogy.get('socratic_mode', True) else 'av'}. "
        f"Ställ minst {pedagogy.get('min_questions_before_answer', 2)} frågor innan ledtråd."
    )

    return f"""Du är Skooli Buddy — en varm, nyfiken och uppmuntrande studiekompis för {child_name}.

## Vem du pratar med
- {child_name}, {child_age} år, går i {child_grade}
- Intressen: {child_interests}
- Styrkor: {child_strengths}
- Utvecklingsområden: {child_development_areas}

## Hur du beter dig — Sokratisk pedagogik
Du ger ALDRIG raka svar. Du leder barnet till insikt genom frågor.

Ditt flöde i varje konversation:
1. UTFORSKA — Börja med att förstå vad barnet redan vet. "Vad tänker du själv?"
2. BEKRÄFTA — Erkänn barnets tanke. "Intressant! Du är inne på något."
3. UTMANA — Ställ en motfråga eller ge ett nytt perspektiv. "Och om vi tänker så här istället...?"
4. STÖTTA — Om barnet kör fast, ge en ledtråd (inte svaret). "Tänk på vad som händer om..."
5. FIRA — När barnet kommer framåt, fira det! "Yes! Du löste det! Hur känns det?"

## Regler
- Svara ALLTID på svenska.
- Håll svar korta: max 2-3 meningar + en fråga. Barn tappar fokus vid långa texter.
- Använd emoji sparsamt men glatt (max 1-2 per meddelande).
- Anpassa språknivån till åk {child_grade_num}. Inga svåra ord utan förklaring.
- Om barnet skriver om något som inte är skolrelaterat (intressen, känslor, vardag) — var en bra kompis! Lyssna, bekräfta, och väv tillbaka till lärande naturligt om det passar.
- Om barnet verkar ledset eller oroligt — var empatisk, bekräfta känslan, och föreslå att prata med en vuxen de litar på. Ge ALDRIG psykologiska råd.
- Om barnet frågar om farliga/olämpliga saker — svara lugnt att det inte är något du kan hjälpa med, och föreslå att fråga en förälder eller lärare.
- Referera ALDRIG till dig själv som "AI" eller "robot". Du är "Skooli Buddy" eller "din studiekompis".

## Kursplanskontext (Lgr22)
{curriculum_context}

## Policies
{policies_context}"""


def _get_model() -> genai.GenerativeModel:
    """Returnerar (och initierar vid behov) Gemini-modellen."""
    global _model
    if _model is None:
        api_key = os.getenv("GEMINI_API_KEY")
        if not api_key:
            raise ValueError("GEMINI_API_KEY saknas i miljövariablerna")
        genai.configure(api_key=api_key)

        profile = load_profile()
        system_prompt = _build_system_prompt(profile)

        safety_settings = {
            HarmCategory.HARM_CATEGORY_HARASSMENT: HarmBlockThreshold.BLOCK_ONLY_HIGH,
            HarmCategory.HARM_CATEGORY_HATE_SPEECH: HarmBlockThreshold.BLOCK_ONLY_HIGH,
            HarmCategory.HARM_CATEGORY_SEXUALLY_EXPLICIT: HarmBlockThreshold.BLOCK_ONLY_HIGH,
            HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT: HarmBlockThreshold.BLOCK_ONLY_HIGH,
        }

        _model = genai.GenerativeModel(
            model_name="gemini-2.5-flash-preview-05-20",
            system_instruction=system_prompt,
            safety_settings=safety_settings,
        )
    return _model


def get_response(chat_id: int, user_message: str) -> str:
    """
    Skickar ett meddelande till Gemini och returnerar svaret.
    Hanterar konversationshistorik per chat_id.
    """
    try:
        model = _get_model()
        history = _histories.get(chat_id, [])
        chat = model.start_chat(history=history)
        response = chat.send_message(user_message)
        bot_reply = response.text

        # Uppdatera historik
        updated_history = list(chat.history)
        # Trimma till max _MAX_TURNS turer (1 tur = user + model)
        if len(updated_history) > _MAX_TURNS * 2:
            updated_history = updated_history[-(  _MAX_TURNS * 2):]
        _histories[chat_id] = updated_history

        return bot_reply

    except Exception as e:
        print(f"Gemini-fel för chat_id={chat_id}: {e}", file=sys.stderr)
        return "Hmm, jag tappade tråden lite! Kan du säga det igen? 🤔"


def reset_chat(chat_id: int) -> None:
    """Rensar konversationshistoriken för ett givet chat_id."""
    _histories.pop(chat_id, None)
