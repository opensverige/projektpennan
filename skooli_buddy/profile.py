"""
Laddar barnets profil, policies och valfritt kursplanspack.
Exponerar allt som ett enkelt dict som kan stoppas i prompten.
Lgr22 är ett pack, inte överhet — tom curriculum-pekare = ingen kursplan.
"""
import json
from pathlib import Path

CONFIG_DIR = Path(__file__).parent.parent / "config"


def load_profile() -> dict:
    """Returnerar dict med keys: child, policies, curriculum"""
    child = json.loads((CONFIG_DIR / "child_profile.json").read_text(encoding="utf-8"))
    policies = json.loads((CONFIG_DIR / "policies.json").read_text(encoding="utf-8"))

    curriculum = []
    curriculum_pack = policies.get("packs", {}).get("curriculum")
    if curriculum_pack:
        lgr22_dir = CONFIG_DIR / "lgr22"
        for f in lgr22_dir.glob("*.json"):
            curriculum.extend(json.loads(f.read_text(encoding="utf-8")))

    return {"child": child, "policies": policies, "curriculum": curriculum}
