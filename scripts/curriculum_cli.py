"""
CLI för import och validering av Lgr22-curriculumdata.
Använd: python scripts/curriculum_cli.py [list|validate|add]
"""

import json
import sys
import argparse
from pathlib import Path

CONFIG_DIR = Path(__file__).parent.parent / "config" / "lgr22"


def list_curriculum() -> None:
    """Lista alla curriculumposter."""
    entries = []
    for f in CONFIG_DIR.glob("*.json"):
        data = json.loads(f.read_text(encoding="utf-8"))
        entries.extend(data)

    print(f"\nTotalt: {len(entries)} curriculumposter\n")
    for e in entries:
        print(f"  [{e['id']}] {e.get('subject', '?')} åk{e.get('grade', '?')} — {e['area']}")


def validate_curriculum() -> bool:
    """Validera att alla JSON-filer har rätt schema."""
    required_keys = {"id", "area", "content", "keywords", "source"}
    errors = []

    for f in CONFIG_DIR.glob("*.json"):
        data = json.loads(f.read_text(encoding="utf-8"))
        if not isinstance(data, list):
            errors.append(f"{f.name}: Förväntade lista, fick {type(data).__name__}")
            continue
        for i, entry in enumerate(data):
            missing = required_keys - set(entry.keys())
            if missing:
                errors.append(f"{f.name}[{i}]: Saknar nycklar: {missing}")

    if errors:
        print("Valideringsfel:")
        for e in errors:
            print(f"  ✗ {e}")
        return False

    print("✓ Alla curriculumfiler är giltiga")
    return True


def main() -> None:
    parser = argparse.ArgumentParser(description="Skooli Buddy Curriculum CLI")
    parser.add_argument("command", choices=["list", "validate"], help="Kommando att köra")
    args = parser.parse_args()

    if args.command == "list":
        list_curriculum()
    elif args.command == "validate":
        ok = validate_curriculum()
        sys.exit(0 if ok else 1)


if __name__ == "__main__":
    main()
