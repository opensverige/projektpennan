#!/usr/bin/env python3
"""
Research pipeline för Skooli Buddy.

Läser findings + sources från disk. Inget nätverk.
Använd: python scripts/research_pipeline.py [sources|list|validate|summary|backlog|new]
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from collections import defaultdict
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
RESEARCH = ROOT / "research"
FINDINGS_DIR = RESEARCH / "findings"
SOURCES_FILE = RESEARCH / "sources.json"
SCHEMA_FILE = RESEARCH / "schema" / "finding.schema.json"
TEMPLATE_FILE = RESEARCH / "templates" / "finding.json"
BACKLOG_FILE = ROOT / "docs" / "BACKLOG.md"

THEMES = {"pedagogy", "safety", "privacy", "product", "curriculum", "accessibility"}
STATUSES = {"draft", "accepted", "superseded"}
CONFIDENCE = {"high", "medium", "low"}
ID_RE = re.compile(r"^[a-z0-9][a-z0-9-]{2,80}$")
DATE_RE = re.compile(r"^[0-9]{4}-[0-9]{2}-[0-9]{2}$")
BACKLOG_RE = re.compile(r"^P-[0-9]{2}$")
BACKLOG_HEADING_RE = re.compile(r"\*\*P-(\d{2})\*\*|P-(\d{2})\b")


def load_json(path: Path) -> object:
    return json.loads(path.read_text(encoding="utf-8"))


def finding_paths() -> list[Path]:
    return sorted(FINDINGS_DIR.glob("*.json"))


def load_findings() -> list[dict]:
    findings = []
    for path in finding_paths():
        data = load_json(path)
        if not isinstance(data, dict):
            raise ValueError(f"{path.name}: förväntade objekt, fick {type(data).__name__}")
        data["_path"] = str(path.relative_to(ROOT))
        findings.append(data)
    return findings


def load_sources() -> dict:
    payload = load_json(SOURCES_FILE)
    if not isinstance(payload, dict) or "sources" not in payload:
        raise ValueError("sources.json saknar nyckeln sources")
    return payload


def cmd_sources() -> int:
    payload = load_sources()
    print(f"\n{len(payload['sources'])} källor\n")
    for src in payload["sources"]:
        themes = ", ".join(src.get("themes", []))
        print(f"  [{src['id']}] {src['org']} — {src['title']}")
        print(f"           {src['url']}")
        print(f"           teman: {themes}  |  takt: {src.get('cadence', '?')}\n")
    return 0


def cmd_list() -> int:
    findings = load_findings()
    print(f"\n{len(findings)} fynd\n")
    for f in findings:
        refs = ",".join(f.get("backlog_refs") or []) or "—"
        print(
            f"  [{f['status']:10}] {f['id']:28}  {f['theme']:14}  "
            f"{f['confidence']:6}  {refs}"
        )
        print(f"             {f['claim'][:100]}")
    print()
    return 0


def _err(errors: list[str], msg: str) -> None:
    errors.append(msg)


def validate_finding(finding: dict, known_urls: set[str], backlog_ids: set[str]) -> list[str]:
    errors: list[str] = []
    path = finding.get("_path", finding.get("id", "?"))

    required = [
        "id", "date", "theme", "status", "claim",
        "evidence", "implication", "backlog_refs", "confidence",
    ]
    for key in required:
        if key not in finding:
            _err(errors, f"{path}: saknar '{key}'")

    if "id" in finding and not ID_RE.match(str(finding["id"])):
        _err(errors, f"{path}: ogiltigt id '{finding['id']}'")

    if "date" in finding and not DATE_RE.match(str(finding["date"])):
        _err(errors, f"{path}: ogiltigt datum '{finding['date']}'")

    if finding.get("theme") not in THEMES:
        _err(errors, f"{path}: okänt tema '{finding.get('theme')}'")

    if finding.get("status") not in STATUSES:
        _err(errors, f"{path}: okänd status '{finding.get('status')}'")

    if finding.get("confidence") not in CONFIDENCE:
        _err(errors, f"{path}: okänd confidence '{finding.get('confidence')}'")

    claim = finding.get("claim", "")
    if not isinstance(claim, str) or len(claim) < 20:
        _err(errors, f"{path}: claim för kort")

    implication = finding.get("implication", "")
    if not isinstance(implication, str) or len(implication) < 20:
        _err(errors, f"{path}: implication för kort")

    evidence = finding.get("evidence")
    if not isinstance(evidence, list) or len(evidence) < 1:
        _err(errors, f"{path}: evidence måste vara en icke-tom lista")
    else:
        for i, item in enumerate(evidence):
            if not isinstance(item, dict):
                _err(errors, f"{path}: evidence[{i}] är inte objekt")
                continue
            for key in ("title", "url", "year", "notes"):
                if key not in item:
                    _err(errors, f"{path}: evidence[{i}] saknar '{key}'")
            url = str(item.get("url", ""))
            if url and not url.startswith(("http://", "https://")):
                _err(errors, f"{path}: evidence[{i}].url måste vara http(s)")
            year = item.get("year")
            if year is not None and (not isinstance(year, int) or year < 1990 or year > 2100):
                _err(errors, f"{path}: evidence[{i}].year ogiltigt")
            notes = item.get("notes", "")
            if isinstance(notes, str) and len(notes) < 5:
                _err(errors, f"{path}: evidence[{i}].notes för kort")

    refs = finding.get("backlog_refs")
    if refs is None:
        pass
    elif not isinstance(refs, list):
        _err(errors, f"{path}: backlog_refs måste vara lista")
    else:
        for ref in refs:
            if not BACKLOG_RE.match(str(ref)):
                _err(errors, f"{path}: ogiltig backlog-ref '{ref}'")
            elif backlog_ids and ref not in backlog_ids:
                _err(errors, f"{path}: {ref} finns inte i docs/BACKLOG.md")

    extra = set(finding) - set(required) - {"_path", "superseded_by"}
    if extra:
        _err(errors, f"{path}: okända fält: {sorted(extra)}")

    if finding.get("status") == "superseded" and not finding.get("superseded_by"):
        _err(errors, f"{path}: superseded kräver superseded_by")

    return errors


def extract_backlog_ids(text: str) -> set[str]:
    ids = set()
    for match in re.finditer(r"\bP-(\d{2})\b", text):
        ids.add(f"P-{match.group(1)}")
    return ids


def cmd_validate() -> int:
    schema = load_json(SCHEMA_FILE)
    if not isinstance(schema, dict):
        print("schema/finding.schema.json är trasig", file=sys.stderr)
        return 1

    sources = load_sources()
    known_urls = {s["url"] for s in sources["sources"] if s.get("url")}
    backlog_ids = extract_backlog_ids(BACKLOG_FILE.read_text(encoding="utf-8")) if BACKLOG_FILE.exists() else set()

    findings = load_findings()
    if not findings:
        print("Inga fynd i research/findings/", file=sys.stderr)
        return 1

    errors: list[str] = []
    seen_ids: dict[str, str] = {}
    for finding in findings:
        fid = finding.get("id")
        if isinstance(fid, str):
            if fid in seen_ids:
                errors.append(f"duplicerat id '{fid}' i {finding['_path']} och {seen_ids[fid]}")
            else:
                seen_ids[fid] = finding["_path"]
            expected_name = f"{fid}.json"
            if Path(finding["_path"]).name != expected_name:
                errors.append(f"{finding['_path']}: filnamn ska vara {expected_name}")
        errors.extend(validate_finding(finding, known_urls, backlog_ids))

    source_ids = [s.get("id") for s in sources["sources"]]
    if len(source_ids) != len(set(source_ids)):
        errors.append("sources.json har duplicerade id")

    if errors:
        print("Valideringsfel:")
        for e in errors:
            print(f"  ✗ {e}")
        return 1

    print(f"✓ {len(findings)} fynd och {len(sources['sources'])} källor är giltiga")
    return 0


def cmd_summary() -> int:
    findings = load_findings()
    by_theme: dict[str, list[dict]] = defaultdict(list)
    for f in findings:
        by_theme[f.get("theme", "?")].append(f)

    print("\nResearch-läge\n")
    for theme in sorted(by_theme):
        rows = by_theme[theme]
        accepted = sum(1 for r in rows if r.get("status") == "accepted")
        print(f"  {theme}: {len(rows)} fynd ({accepted} accepted)")
        for r in rows:
            mark = "●" if r.get("status") == "accepted" else "○"
            print(f"    {mark} {r['id']} — {r['claim'][:90]}")
        print()
    return 0


def cmd_backlog() -> int:
    findings = load_findings()
    print("\nImplikationer → backlog\n")
    for f in sorted(findings, key=lambda x: x.get("id", "")):
        if f.get("status") == "superseded":
            continue
        refs = ", ".join(f.get("backlog_refs") or []) or "—"
        print(f"  {f['id']}  →  {refs}")
        print(f"    {f['implication']}\n")
    return 0


def cmd_new(finding_id: str, title: str, theme: str) -> int:
    if not ID_RE.match(finding_id):
        print("id måste vara kebab-case, 3–81 tecken", file=sys.stderr)
        return 1
    if theme not in THEMES:
        print(f"tema måste vara ett av: {', '.join(sorted(THEMES))}", file=sys.stderr)
        return 1

    dest = FINDINGS_DIR / f"{finding_id}.json"
    if dest.exists():
        print(f"{dest} finns redan", file=sys.stderr)
        return 1

    template = load_json(TEMPLATE_FILE)
    template["id"] = finding_id
    template["date"] = date.today().isoformat()
    template["theme"] = theme
    template["claim"] = title if len(title) >= 20 else f"{title} — fyll på med ett prövbart påstående."
    template["implication"] = "Beskriv vad som ändras i produkt, regler eller backlog."
    dest.write_text(json.dumps(template, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    try:
        shown = dest.relative_to(ROOT)
    except ValueError:
        shown = dest
    print(f"Skapade {shown}")
    print("Fyll evidence + implication, kör sedan: python scripts/research_pipeline.py validate")
    return 0


def main() -> int:
    parser = argparse.ArgumentParser(description="Skooli Buddy research pipeline")
    parser.add_argument(
        "command",
        choices=["sources", "list", "validate", "summary", "backlog", "new"],
    )
    parser.add_argument("--id", dest="finding_id", help="id för new")
    parser.add_argument("--title", default="Nytt påstående", help="claim-utkast för new")
    parser.add_argument("--theme", default="pedagogy", help="tema för new")
    args = parser.parse_args()

    try:
        if args.command == "sources":
            return cmd_sources()
        if args.command == "list":
            return cmd_list()
        if args.command == "validate":
            return cmd_validate()
        if args.command == "summary":
            return cmd_summary()
        if args.command == "backlog":
            return cmd_backlog()
        if args.command == "new":
            if not args.finding_id:
                print("--id krävs för new", file=sys.stderr)
                return 1
            return cmd_new(args.finding_id, args.title, args.theme)
    except (OSError, json.JSONDecodeError, ValueError) as exc:
        print(f"Fel: {exc}", file=sys.stderr)
        return 1
    return 1


if __name__ == "__main__":
    sys.exit(main())
