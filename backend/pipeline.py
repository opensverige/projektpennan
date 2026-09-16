"""
Huvudpipelinen. Ett meddelande in, ett svar ut.
Steg: preflight -> safety_in -> rag -> llm -> safety_out -> log -> respond

LLM:en undervisar. Koden validerar. Föräldern bestämmer.
"""

import json
import hashlib
import hmac
import os
import secrets
from datetime import datetime, timezone
from pathlib import Path
from safety import (
    check_input_safety,
    check_output_safety,
    kernel_reply,
    load_policies,
)
from rag import search_curriculum
from providers import complete, load_runtime

VAULT_PATH = Path(os.getenv("VAULT_PATH", "/app/vault"))
AUDIT_SECRET_FILE = VAULT_PATH / "config" / "audit-secret.txt"
_AUDIT_SECRET: str | None = None


def load_child_profile() -> dict:
    profile_path = VAULT_PATH / "config" / "child-profile.json"
    if not profile_path.exists():
        raise FileNotFoundError(f"CRITICAL: {profile_path} saknas.")
    return json.loads(profile_path.read_text(encoding="utf-8"))


def build_system_prompt(profile: dict, policies: dict) -> str:
    """
    Bygg systemprompten från SOUL.md + SKILL.md + RULES.md + barnets profil.
    """
    agents_path = Path("/app/agents/tutor")

    soul = (agents_path / "SOUL.md").read_text(encoding="utf-8")
    skill = (agents_path / "SKILL.md").read_text(encoding="utf-8")
    rules = (agents_path / "RULES.md").read_text(encoding="utf-8")

    child = profile.get("child", {})
    pedagogy = policies.get("pedagogy", {})
    packs = policies.get("packs", {})
    accommodations = child.get("accommodations") or {}
    acc_notes = ""
    if accommodations.get("parent_authored") and (
        accommodations.get("notes") or accommodations.get("labels")
    ):
        acc_notes = accommodations.get("notes") or ", ".join(
            accommodations.get("labels") or []
        )
        if not accommodations.get("tell_child_the_label"):
            acc_notes = f"Anpassa tyst efter: {acc_notes}. Nämn inte etiketten."

    context_block = f"""
## Aktuell elev
- Namn: {child.get('display_name', 'Elev')}
- Årskurs: {child.get('grade', '?')}
- Ålder: {child.get('age', '?')}
- Ämnen: {', '.join(child.get('subjects', []))}
- Intressen: {', '.join(child.get('interests', []))}
- Stödpreferenser: {', '.join(child.get('support_preferences', []))}
- Förälder-skriven anpassning: {acc_notes or 'ingen — extra-stöd-default'}

## Packs (föräldern styr)
- Kursplan: {packs.get('curriculum') or 'av — hjälp ändå, åberopa inte skolan'}
- Kursplan är överhet: {'JA' if packs.get('curriculum_required') else 'NEJ'}
- Världsbild: {packs.get('worldview') or 'ingen — var kort, ta inte ställning'}
- Egen agent: {packs.get('custom_agent') or 'ingen'}
- Skolkontext: {packs.get('school_context') or 'ingen — gissa inte vad skolan gör, nudge:a inte'}

## Pedagogiska inställningar
- Tillåtna metoder: {', '.join(pedagogy.get('allowed_modes', []))}
- Sokratiskt läge: {'JA' if pedagogy.get('socratic_mode') else 'NEJ'}
- Frågor innan ledtråd: {pedagogy.get('min_questions_before_answer', 2)}
- Frågor innan förklaring: {pedagogy.get('max_questions_before_hint', 4)}
- Nudge läxa: {'JA' if pedagogy.get('nudge_homework') else 'NEJ — barnet öppnar själv'}
"""

    return f"{soul}\n\n---\n\n{skill}\n\n---\n\n{rules}\n\n---\n\n{context_block}"


def log_conversation_turn(session_id: str, role: str, content: str, metadata: dict = None):
    """
    Write-once logging. Append till sessionens fil.
    Varje rad är en JSON-rad (JSONL-format).
    """
    conv_dir = VAULT_PATH / "conversations"
    conv_dir.mkdir(parents=True, exist_ok=True)

    filepath = conv_dir / f"{session_id}.jsonl"

    entry = {
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "role": role,
        "content": content,
        "metadata": metadata or {}
    }

    line = json.dumps(entry, ensure_ascii=False) + "\n"

    # Atomisk append (tillräckligt för MVP, inte temp+rename behövs för append)
    with open(filepath, "a", encoding="utf-8") as f:
        f.write(line)


def get_audit_secret() -> str:
    global _AUDIT_SECRET
    if _AUDIT_SECRET:
        return _AUDIT_SECRET
    AUDIT_SECRET_FILE.parent.mkdir(parents=True, exist_ok=True)
    if not AUDIT_SECRET_FILE.exists():
        AUDIT_SECRET_FILE.write_text(secrets.token_hex(32), encoding="utf-8")
    secret = AUDIT_SECRET_FILE.read_text(encoding="utf-8").strip()
    if not secret:
        secret = secrets.token_hex(32)
        AUDIT_SECRET_FILE.write_text(secret, encoding="utf-8")
    _AUDIT_SECRET = secret
    return secret


def log_audit(session_id: str, action: str, details: str):
    """
    Append-only audit log med hashkedja.
    """
    audit_dir = VAULT_PATH / "audit"
    audit_dir.mkdir(parents=True, exist_ok=True)
    audit_file = audit_dir / "audit.log"

    # Läs sista hash
    prev_hash = "genesis"
    if audit_file.exists():
        lines = audit_file.read_text(encoding="utf-8").strip().split("\n")
        if lines and lines[-1].strip():
            try:
                last_entry = json.loads(lines[-1])
                prev_hash = last_entry.get("hash", "genesis")
            except json.JSONDecodeError:
                prev_hash = "chain_broken"

    entry = {
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "session_id": session_id,
        "action": action,
        "details": details,
        "prev_hash": prev_hash
    }

    base_raw = json.dumps(entry, ensure_ascii=False, sort_keys=True)
    entry["hash"] = hashlib.sha256(base_raw.encode()).hexdigest()
    secret = get_audit_secret()
    signed_raw = json.dumps(entry, ensure_ascii=False, sort_keys=True)
    entry["signature"] = hmac.new(secret.encode("utf-8"), signed_raw.encode("utf-8"), hashlib.sha256).hexdigest()

    line = json.dumps(entry, ensure_ascii=False) + "\n"

    with open(audit_file, "a", encoding="utf-8") as f:
        f.write(line)


async def run_pipeline(
    session_id: str,
    user_message: str,
    history: list[dict],
    api_key: str | None = None,
    provider: str | None = None,
) -> dict:
    """
    Hela pipelinen. Ett meddelande in, ett resultat ut.

    Returnerar:
    {
        "status": "ok" | "blocked_input" | "blocked_output" | "error",
        "response": str,
        "processing_chain": dict   # för debugging/audit
    }
    """
    chain = {
        "input": user_message,
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "steps": []
    }

    # --- STEG 1: Preflight ---
    policies = load_policies()
    profile = load_child_profile()
    chain["steps"].append({"step": "preflight", "status": "ok"})

    # --- STEG 2: Input safety ---
    input_check = check_input_safety(user_message)
    chain["steps"].append({"step": "safety_in", "result": input_check})

    if not input_check["safe"]:
        kind = input_check.get("kind") or "block"
        safe_response = kernel_reply(kind)
        log_conversation_turn(session_id, "user", user_message, {"blocked": True, "kind": kind})
        log_conversation_turn(session_id, "assistant", safe_response)
        log_audit(session_id, "INPUT_BLOCKED", input_check["reason"])
        chain["steps"].append({"step": "respond", "type": "blocked_input", "kind": kind})
        return {"status": "blocked_input", "response": safe_response, "processing_chain": chain}

    # --- STEG 3: RAG mot kursplanspack (av om föräldern stängt packen) ---
    child_info = profile.get("child", {})
    curriculum_pack = policies.get("packs", {}).get("curriculum")
    if curriculum_pack:
        rag_result = await search_curriculum(
            query=user_message,
            grade=child_info.get("grade"),
            subject=None,
            top_k=3,
        )
    else:
        rag_result = {
            "context": "",
            "hits": 0,
            "status": "skipped",
            "reason": "curriculum_pack_off",
        }
    rag_context = rag_result.get("context", "")
    chain["steps"].append(
        {
            "step": "rag",
            "status": rag_result.get("status", "unknown"),
            "hits": rag_result.get("hits", 0),
            "reason": rag_result.get("reason"),
        }
    )

    # --- STEG 4: LLM Inference ---
    system_prompt = build_system_prompt(profile, policies)
    conversation = history.copy()
    if rag_context:
        conversation.append({"role": "system", "content": f"[Kursplan]\n{rag_context}"})
    conversation.append({"role": "user", "content": user_message})

    runtime = load_runtime(override_key=api_key, override_provider=provider)
    try:
        llm_response = await complete(system_prompt, conversation, runtime)
        chain["steps"].append({"step": "llm", "status": "ok", "model": runtime.label()})
    except Exception as e:
        log_audit(session_id, "LLM_ERROR", type(e).__name__)
        chain["steps"].append({"step": "llm", "status": "error", "error": type(e).__name__})
        return {
            "status": "error",
            "response": "Oj, jag tappade tråden. Kan du försöka igen?",
            "processing_chain": chain,
            "model": runtime.label(),
        }

    # --- STEG 5: Output safety ---
    output_check = check_output_safety(llm_response, policies)
    chain["steps"].append({"step": "safety_out", "result": output_check})

    if not output_check["safe"]:
        max_retries = policies.get("safety", {}).get("max_retries_on_unsafe_output", 2)
        retry_count = 0
        while not output_check["safe"] and retry_count < max_retries:
            retry_count += 1
            retry_msg = conversation + [
                {"role": "assistant", "content": llm_response},
                {"role": "user", "content": "[SYSTEM] Ditt svar bröt mot säkerhetsreglerna. Formulera om ditt svar."}
            ]
            try:
                llm_response = await complete(system_prompt, retry_msg, runtime)
                output_check = check_output_safety(llm_response, policies)
            except Exception:
                break

        if not output_check["safe"]:
            safe_response = "Jag behöver tänka lite mer på det där. Kan vi prata om något annat?"
            log_audit(session_id, "OUTPUT_BLOCKED", f"After {retry_count} retries")
            chain["steps"].append({"step": "respond", "type": "blocked_output"})
            return {
                "status": "blocked_output",
                "response": safe_response,
                "processing_chain": chain,
                "model": runtime.label(),
            }

    # Använd trimmad version om den fanns
    final_response = output_check.get("trimmed") or llm_response

    # --- STEG 6: Log ---
    log_conversation_turn(session_id, "user", user_message)
    log_conversation_turn(session_id, "assistant", final_response, {
        "model": runtime.label(),
        "rag_used": bool(rag_context),
        "rag_hits": rag_result.get("hits", 0)
    })
    log_audit(session_id, "RESPONSE_SENT", f"Length: {len(final_response)} chars")
    chain["steps"].append({"step": "log", "status": "ok"})

    return {
        "status": "ok",
        "response": final_response,
        "processing_chain": chain,
        "model": runtime.label(),
    }
