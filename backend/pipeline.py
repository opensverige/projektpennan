"""
Huvudpipelinen. Ett meddelande in, ett svar ut.
Steg: preflight -> safety_in -> rag -> llm -> safety_out -> log -> respond

LLM:en undervisar. Koden validerar. Föräldern bestämmer.
"""

import json
import hashlib
import os
import httpx
from datetime import datetime, timezone
from pathlib import Path
from safety import check_input_safety, check_output_safety, load_policies

VAULT_PATH = Path("/app/vault")
OLLAMA_URL = os.getenv("OLLAMA_URL", "http://ollama:11434")
MODEL_NAME = os.getenv("MODEL_NAME", "hermes3:8b")


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

    context_block = f"""
## Aktuell elev
- Namn: {child.get('display_name', 'Elev')}
- Årskurs: {child.get('grade', '?')}
- Ålder: {child.get('age', '?')}
- Ämnen: {', '.join(child.get('subjects', []))}
- Intressen: {', '.join(child.get('interests', []))}

## Pedagogiska inställningar
- Sokratiskt läge: {'JA' if policies.get('pedagogy', {}).get('socratic_mode') else 'NEJ'}
- Frågor innan ledtråd: {policies.get('pedagogy', {}).get('min_questions_before_answer', 2)}
- Frågor innan förklaring: {policies.get('pedagogy', {}).get('max_questions_before_hint', 4)}
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

    raw = json.dumps(entry, ensure_ascii=False, sort_keys=True)
    entry["hash"] = hashlib.sha256(raw.encode()).hexdigest()

    line = json.dumps(entry, ensure_ascii=False) + "\n"

    with open(audit_file, "a", encoding="utf-8") as f:
        f.write(line)


async def call_ollama(system_prompt: str, conversation_history: list[dict]) -> str:
    """
    Skicka request till Ollama. Returnerar LLM-svaret som sträng.
    """
    messages = [{"role": "system", "content": system_prompt}]
    messages.extend(conversation_history)

    async with httpx.AsyncClient(timeout=120.0) as client:
        response = await client.post(
            f"{OLLAMA_URL}/api/chat",
            json={
                "model": MODEL_NAME,
                "messages": messages,
                "stream": False,
                "options": {
                    "temperature": 0.7,
                    "num_predict": 512,
                }
            }
        )
        response.raise_for_status()
        data = response.json()
        return data.get("message", {}).get("content", "")


async def run_pipeline(session_id: str, user_message: str, history: list[dict]) -> dict:
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
        safe_response = "Hmm, den frågan kan jag inte hjälpa till med. Vill du fråga om något annat?"
        log_conversation_turn(session_id, "user", user_message, {"blocked": True})
        log_conversation_turn(session_id, "assistant", safe_response)
        log_audit(session_id, "INPUT_BLOCKED", input_check["reason"])
        chain["steps"].append({"step": "respond", "type": "blocked_input"})
        return {"status": "blocked_input", "response": safe_response, "processing_chain": chain}

    # --- STEG 3: RAG (placeholder tills Chroma är uppsatt) ---
    rag_context = ""  # TODO: Implementera RAG-sökning mot curriculum-vectors
    chain["steps"].append({"step": "rag", "status": "skipped", "reason": "not_implemented"})

    # --- STEG 4: LLM Inference ---
    system_prompt = build_system_prompt(profile, policies)
    conversation = history + [{"role": "user", "content": user_message}]

    try:
        llm_response = await call_ollama(system_prompt, conversation)
        chain["steps"].append({"step": "llm", "status": "ok", "model": MODEL_NAME})
    except Exception as e:
        log_audit(session_id, "LLM_ERROR", str(e))
        chain["steps"].append({"step": "llm", "status": "error", "error": str(e)})
        return {
            "status": "error",
            "response": "Oj, jag tappade tråden. Kan du försöka igen?",
            "processing_chain": chain
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
                llm_response = await call_ollama(system_prompt, retry_msg)
                output_check = check_output_safety(llm_response, policies)
            except Exception:
                break

        if not output_check["safe"]:
            safe_response = "Jag behöver tänka lite mer på det där. Kan vi prata om något annat?"
            log_audit(session_id, "OUTPUT_BLOCKED", f"After {retry_count} retries")
            chain["steps"].append({"step": "respond", "type": "blocked_output"})
            return {"status": "blocked_output", "response": safe_response, "processing_chain": chain}

    # Använd trimmad version om den fanns
    final_response = output_check.get("trimmed") or llm_response

    # --- STEG 6: Log ---
    log_conversation_turn(session_id, "user", user_message)
    log_conversation_turn(session_id, "assistant", final_response, {
        "model": MODEL_NAME,
        "rag_used": bool(rag_context)
    })
    log_audit(session_id, "RESPONSE_SENT", f"Length: {len(final_response)} chars")
    chain["steps"].append({"step": "log", "status": "ok"})

    return {"status": "ok", "response": final_response, "processing_chain": chain}
