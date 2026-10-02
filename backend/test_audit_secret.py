import pipeline


def test_audit_key_reuses_existing_file(tmp_path, monkeypatch):
    monkeypatch.setattr(pipeline, "VAULT_PATH", tmp_path)
    monkeypatch.setattr(pipeline, "_AUDIT_SECRET", None)
    path = tmp_path / "config" / "audit-secret.txt"
    path.parent.mkdir()
    path.write_text("already-there\n", encoding="utf-8")
    assert pipeline.get_audit_secret() == "already-there"
    monkeypatch.setattr(pipeline, "_AUDIT_SECRET", None)
    assert pipeline.get_audit_secret() == "already-there"


def test_audit_key_is_owner_only_and_stable(tmp_path, monkeypatch):
    monkeypatch.setattr(pipeline, "VAULT_PATH", tmp_path)
    monkeypatch.setattr(pipeline, "_AUDIT_SECRET", None)
    first = pipeline.get_audit_secret()
    path = tmp_path / "config" / "audit-secret.txt"
    assert path.is_file()
    assert path.stat().st_mode & 0o777 == 0o600
    assert path.read_text(encoding="utf-8") == first
    monkeypatch.setattr(pipeline, "_AUDIT_SECRET", None)
    assert pipeline.get_audit_secret() == first


def test_log_audit_still_signs(tmp_path, monkeypatch):
    monkeypatch.setattr(pipeline, "VAULT_PATH", tmp_path)
    monkeypatch.setattr(pipeline, "_AUDIT_SECRET", None)
    pipeline.log_audit("s1", "RESPONSE_SENT", "ok")
    line = (tmp_path / "audit" / "audit.log").read_text(encoding="utf-8").strip()
    entry = __import__("json").loads(line)
    assert entry["signature"]
    assert entry["hash"]
    assert entry["action"] == "RESPONSE_SENT"
