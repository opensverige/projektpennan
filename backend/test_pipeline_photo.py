import asyncio
import base64

from pipeline import parse_image, run_pipeline


def test_parse_image_rejects_giant():
    blob = base64.b64encode(b"x" * 400_000).decode()
    try:
        parse_image(blob)
        raise AssertionError("should reject")
    except ValueError:
        pass


def test_parse_image_reads_data_url():
    raw = b"\x89PNG" + b"abcd" * 20
    b64 = base64.b64encode(raw).decode()
    data, mime = parse_image(f"data:image/png;base64,{b64}")
    assert mime == "image/png"
    assert data == b64


def test_pipeline_sends_photo_not_bytes_in_log(tmp_path, monkeypatch):
    monkeypatch.setattr("pipeline.VAULT_PATH", tmp_path)
    monkeypatch.setattr(
        "pipeline.load_policies",
        lambda: {"packs": {}, "pedagogy": {}, "safety": {}},
    )
    monkeypatch.setattr(
        "pipeline.load_child_profile",
        lambda: {
            "schema_version": "0.2.0",
            "child": {"display_name": "Alma", "interests": ["Minecraft"]},
        },
    )
    monkeypatch.setattr("pipeline.maybe_note_from_child", lambda msg: None)
    monkeypatch.setattr(
        "pipeline.build_system_prompt",
        lambda profile, policies: "Du är Utter.",
    )
    captured = {}

    async def fake_complete(system, history, runtime=None, image=None, image_mime=None):
        captured["image"] = image
        captured["system"] = system
        return "Minecraft. Bilden är inne. Vad är dimma?"

    monkeypatch.setattr("pipeline.complete", fake_complete)
    monkeypatch.setattr("pipeline.load_runtime", lambda **kw: type("R", (), {"label": lambda self: "test"})())
    raw = b"\xff\xd8\xff" + b"abcd" * 40
    photo = "data:image/jpeg;base64," + base64.b64encode(raw).decode()
    result = asyncio.run(
        run_pipeline("s1", "foto av läxan", [], image=photo)
    )
    assert result["status"] == "ok"
    assert captured["image"]
    assert "ansikten" in captured["system"]
    log = (tmp_path / "conversations" / "s1.jsonl").read_text(encoding="utf-8")
    assert "foto av läxan" in log
    assert captured["image"] not in log
