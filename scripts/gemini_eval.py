"""
Benchmark-skript för att utvärdera Skooli Buddy mot testfrågor.
Kör: python scripts/gemini_eval.py
"""

import os
import sys
import json
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

# Lägg till projektrot i path
sys.path.insert(0, str(Path(__file__).parent.parent))


TEST_CASES = [
    {
        "input": "Vad är 7 gånger 8?",
        "expect_not": ["56", "fyrtioåtta", "48"],
        "expect_socratic": True,
        "description": "Ska INTE ge rakt svar på multiplikation",
    },
    {
        "input": "Jag förstår inte bråk alls",
        "expect_contains": ["?"],
        "description": "Ska ställa en fråga för att utforska vad barnet vet",
    },
    {
        "input": "Jag tycker om Minecraft",
        "expect_contains": ["?"],
        "description": "Ska vara vänlig och ställa en fråga",
    },
]


def run_eval() -> None:
    """Kör evaluering mot Gemini-modellen."""
    try:
        import google.generativeai as genai
    except ImportError:
        print("Fel: google-generativeai är inte installerat. Kör: pip install google-generativeai")
        sys.exit(1)

    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        print("Fel: GEMINI_API_KEY saknas i .env")
        sys.exit(1)

    genai.configure(api_key=api_key)

    print("Tillgängliga Flash-modeller:")
    for m in genai.list_models():
        if "flash" in m.name.lower() and "generateContent" in m.supported_generation_methods:
            print(f"  {m.name}")

    print(f"\nKör {len(TEST_CASES)} testfall...\n")

    # Importera core efter att path är satt
    from skooli_buddy.core import get_response, reset_chat

    passed = 0
    failed = 0
    test_chat_id = 99999

    for i, tc in enumerate(TEST_CASES, 1):
        reset_chat(test_chat_id)
        response = get_response(test_chat_id, tc["input"])

        ok = True
        notes = []

        if tc.get("expect_not"):
            for forbidden in tc["expect_not"]:
                if forbidden.lower() in response.lower():
                    ok = False
                    notes.append(f"Innehöll förbjudet svar: '{forbidden}'")

        if tc.get("expect_contains"):
            for required in tc["expect_contains"]:
                if required not in response:
                    ok = False
                    notes.append(f"Saknade förväntat innehåll: '{required}'")

        status = "✓" if ok else "✗"
        print(f"[{i}] {status} {tc['description']}")
        print(f"    Input:  {tc['input']}")
        print(f"    Svar:   {response[:120]}{'...' if len(response) > 120 else ''}")
        if notes:
            for note in notes:
                print(f"    ⚠ {note}")
        print()

        if ok:
            passed += 1
        else:
            failed += 1

    print(f"Resultat: {passed}/{len(TEST_CASES)} godkända")
    sys.exit(0 if failed == 0 else 1)


if __name__ == "__main__":
    run_eval()
