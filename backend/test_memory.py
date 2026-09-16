from memory import interests_of, remember_child, render_for_prompt


def test_remember_writes_obsidian_notes(tmp_path, monkeypatch):
    monkeypatch.setattr("memory.VAULT", tmp_path)
    monkeypatch.setattr("memory.MEMORY", tmp_path / "memory")
    monkeypatch.setattr("memory.PROFILE", tmp_path / "config" / "child-profile.json")
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
    monkeypatch.setattr("memory.VAULT", tmp_path)
    monkeypatch.setattr("memory.MEMORY", tmp_path / "memory")
    monkeypatch.setattr("memory.PROFILE", tmp_path / "config" / "child-profile.json")
    remember_child("Bo", ["Lego", "Lego", "Fotboll"])
    assert interests_of() == ["Lego", "Fotboll"]
