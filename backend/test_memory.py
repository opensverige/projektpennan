from memory import interests_of, remember_child, render_for_prompt


def _vault(tmp_path, monkeypatch):
    monkeypatch.setattr("memory.VAULT", tmp_path)
    monkeypatch.setattr("memory.MEMORY", tmp_path / "memory")
    monkeypatch.setattr("memory.PROFILE", tmp_path / "config" / "child-profile.json")


def test_remember_writes_obsidian_notes(tmp_path, monkeypatch):
    _vault(tmp_path, monkeypatch)
    saved = remember_child("Alma", ["Minecraft", "Hästar"])
    assert saved["name"] == "Alma"
    assert saved["interests"] == ["Minecraft", "Hästar"]
    barn = (tmp_path / "memory" / "barn.md").read_text(encoding="utf-8")
    assert "Alma" in barn
    assert "[[Minecraft]]" in barn
    assert (tmp_path / "memory" / "minecraft.md").is_file()
    prompt = render_for_prompt()
    assert "Minecraft" in prompt
    assert "4+3" in prompt


def test_interests_stay_unique(tmp_path, monkeypatch):
    _vault(tmp_path, monkeypatch)
    remember_child("Bo", ["Lego", "Lego", "Fotboll"])
    assert interests_of() == ["Lego", "Fotboll"]


def test_intake_writes_grade_door_and_overlay(tmp_path, monkeypatch):
    _vault(tmp_path, monkeypatch)
    saved = remember_child(
        "Nour",
        ["Minecraft", "Sport", "Rita & bygga"],
        grade="Åk 5",
        language="Svenska + annat hemma",
        struggle="Matte",
        energy="Slut",
        helps=["Korta steg", "Läs högt"],
        note="kortare pass",
    )
    assert saved["interests"] == ["Minecraft", "Sport"]
    assert saved["grade"] == "Åk 5"
    assert saved["support_preferences"] == ["korta_steg", "las_hogt"]
    barn = (tmp_path / "memory" / "barn.md").read_text(encoding="utf-8")
    assert "Årskurs: Åk 5" in barn
    assert "Kärvar: Matte" in barn
    overlay = (tmp_path / "packs" / "pedagogy" / "OVERLAY.md").read_text(
        encoding="utf-8"
    )
    assert "nudge_homework: false" in overlay
    assert "Slut" in overlay
    prompt = render_for_prompt()
    assert "en takt mot Minecraft" in prompt
    assert "Foto av läxan är en giltig start" in prompt
    profile = (tmp_path / "config" / "child-profile.json").read_text(encoding="utf-8")
    assert "kortare pass" in profile
    assert '"grade": 5' in profile


def test_empty_helps_get_extra_stod_default(tmp_path, monkeypatch):
    _vault(tmp_path, monkeypatch)
    saved = remember_child("Leo", ["Djur & dino"])
    assert saved["support_preferences"] == [
        "korta_steg",
        "en_sak_i_taget",
        "pauser",
    ]
