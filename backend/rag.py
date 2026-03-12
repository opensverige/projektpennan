"""Curriculum Retrieval (RAG) powered by Chroma + Ollama embeddings.

The curriculum data lives under `vault/curriculum-vectors/`.
Each JSON/JSONL file should contain entries formatted as:
{
    "id": "math-4-area",
    "grade": 4,
    "subject": "matematik",
    "title": "Area av rektanglar",
    "content": "Lärandemål ..."
}

Documents are embedded via Ollama's `nomic-embed-text` (configurable via
`EMBED_MODEL`) and stored in a persistent Chroma collection. Queries are
run synchronously; the public `search_curriculum` helper exposes an async
API for the pipeline.
"""

from __future__ import annotations

import asyncio
import hashlib
import json
import os
from pathlib import Path
from typing import Any, Dict, List, Optional

import httpx

try:
    import chromadb
    from chromadb.utils.embedding_functions import EmbeddingFunction
except ImportError:  # pragma: no cover - handled gracefully at runtime
    chromadb = None  # type: ignore
    EmbeddingFunction = object  # type: ignore

VAULT_PATH = Path(os.getenv("VAULT_PATH", "/app/vault"))
CURRICULUM_DIR = VAULT_PATH / "curriculum-vectors"
PERSIST_DIR = CURRICULUM_DIR / "chroma"
OLLAMA_URL = os.getenv("OLLAMA_URL", "http://ollama:11434")
EMBED_MODEL = os.getenv("EMBED_MODEL", "nomic-embed-text")
CURRICULUM_COLLECTION = os.getenv("CURRICULUM_COLLECTION", "lgr22-curriculum")
MAX_SECTION_CHARS = 600


BaseEmbeddingFunction = EmbeddingFunction if isinstance(EmbeddingFunction, type) else object


class OllamaEmbeddingFunction(BaseEmbeddingFunction):
    """Chroma embedding function that proxies to Ollama's embeddings API."""

    def __init__(self, model: str, url: str, timeout: float = 60.0):
        self.model = model
        self.url = url.rstrip("/")
        self.timeout = timeout

    def __call__(self, texts: List[str]) -> List[List[float]]:  # type: ignore[override]
        embeddings: List[List[float]] = []
        with httpx.Client(timeout=self.timeout) as client:
            for text in texts:
                payload = {"model": self.model, "prompt": text}
                resp = client.post(f"{self.url}/api/embeddings", json=payload)
                resp.raise_for_status()
                data = resp.json()
                emb = data.get("embedding")
                if not isinstance(emb, list):  # pragma: no cover - sanity guard
                    raise RuntimeError("Ollama embeddings response saknar 'embedding'.")
                embeddings.append(emb)
        return embeddings


class CurriculumRAG:
    def __init__(self, sources_dir: Path, persist_dir: Path, ollama_url: str, embed_model: str):
        if chromadb is None:
            raise RuntimeError("chromadb saknas — installera backend/requirements.txt")

        self.sources_dir = sources_dir
        self.persist_dir = persist_dir
        self.persist_dir.mkdir(parents=True, exist_ok=True)

        self.embedding_fn = OllamaEmbeddingFunction(embed_model, ollama_url)
        self.client = chromadb.PersistentClient(path=str(self.persist_dir))
        self.collection = self.client.get_or_create_collection(
            name=CURRICULUM_COLLECTION,
            metadata={"hnsw:space": "cosine"},
            embedding_function=self.embedding_fn,
        )
        self.available = False
        self.doc_count = 0
        self._sync_documents()

    # ------------------------------------------------------------------
    # Data loading / syncing
    def _load_source_documents(self) -> List[Dict[str, Any]]:
        docs: List[Dict[str, Any]] = []
        if not self.sources_dir.exists():
            return docs

        for path in sorted(self.sources_dir.glob("*.json")):
            if path.name.endswith(".schema.json"):
                continue
            try:
                payload = json.loads(path.read_text(encoding="utf-8"))
            except json.JSONDecodeError:
                continue
            if isinstance(payload, list):
                docs.extend(self._normalise_entries(payload, path))
            elif isinstance(payload, dict):
                docs.extend(self._normalise_entries([payload], path))

        for path in sorted(self.sources_dir.glob("*.jsonl")):
            with path.open("r", encoding="utf-8") as handle:
                lines = [line.strip() for line in handle if line.strip()]
            entries = []
            for line in lines:
                try:
                    entries.append(json.loads(line))
                except json.JSONDecodeError:
                    continue
            docs.extend(self._normalise_entries(entries, path))
        return docs

    def _normalise_entries(self, entries: List[Dict[str, Any]], origin: Path) -> List[Dict[str, Any]]:
        normalised: List[Dict[str, Any]] = []
        for idx, entry in enumerate(entries):
            content = entry.get("content")
            if not content:
                continue
            doc_id = entry.get("id") or self._entry_hash(origin, idx, content)
            title = entry.get("title") or "Okänd rubrik"
            subject = str(entry.get("subject") or "okänt ämne").strip()
            grade = str(entry.get("grade") or "?").strip()
            normalised.append(
                {
                    "id": str(doc_id),
                    "content": str(content),
                    "title": title,
                    "subject": subject,
                    "subject_key": subject.lower(),
                    "grade": grade,
                }
            )
        return normalised

    @staticmethod
    def _entry_hash(origin: Path, idx: int, content: str) -> str:
        seed = f"{origin}:{idx}:{content[:80]}".encode()
        return hashlib.sha1(seed).hexdigest()

    def _sync_documents(self) -> None:
        docs = self._load_source_documents()
        if not docs:
            self.available = False
            self.doc_count = 0
            return

        ids = [doc["id"] for doc in docs]
        texts = [doc["content"] for doc in docs]
        metadatas = [
            {
                "title": doc["title"],
                "subject": doc["subject"],
                "subject_key": doc.get("subject_key", doc["subject"].lower()),
                "grade": doc["grade"],
            }
            for doc in docs
        ]
        self.collection.upsert(ids=ids, documents=texts, metadatas=metadatas)
        self.available = True
        self.doc_count = len(docs)

    # ------------------------------------------------------------------
    # Query helpers
    def query(self, query_text: str, grade: Optional[str | int] = None, subject: Optional[str] = None,
              top_k: int = 3) -> List[Dict[str, Any]]:
        if not self.available:
            return []

        where: Dict[str, Any] = {}
        if grade:
            where["grade"] = str(grade)
        if subject:
            where["subject_key"] = subject.strip().lower()

        try:
            results = self.collection.query(
                query_texts=[query_text],
                n_results=top_k,
                where=where or None,
            )
        except Exception:
            return []

        documents = results.get("documents") or [[]]
        metadatas = results.get("metadatas") or [[]]
        output: List[Dict[str, Any]] = []
        for idx, content in enumerate(documents[0]):
            meta = metadatas[0][idx] if idx < len(metadatas[0]) else {}
            cleaned = (content or "").strip()
            if not cleaned:
                continue
            output.append(
                {
                    "content": cleaned,
                    "title": meta.get("title", ""),
                    "subject": meta.get("subject", ""),
                    "grade": meta.get("grade", ""),
                }
            )
        return output

    @staticmethod
    def format_results(results: List[Dict[str, Any]]) -> str:
        if not results:
            return ""
        sections: List[str] = []
        for item in results:
            content = item["content"].strip().replace("\n", " ")
            if len(content) > MAX_SECTION_CHARS:
                content = content[:MAX_SECTION_CHARS].rstrip() + " …"
            title = item.get("title") or "Curriculum"
            grade = item.get("grade") or "?"
            subject = item.get("subject") or "ämne"
            sections.append(f"{title} (åk {grade}, {subject}): {content}")
        return "\n".join(sections)


_rag_instance: Optional[CurriculumRAG] = None


def _get_rag_instance() -> Optional[CurriculumRAG]:
    global _rag_instance
    if _rag_instance is not None:
        return _rag_instance
    if chromadb is None:
        return None
    try:
        _rag_instance = CurriculumRAG(
            sources_dir=CURRICULUM_DIR,
            persist_dir=PERSIST_DIR,
            ollama_url=OLLAMA_URL,
            embed_model=EMBED_MODEL,
        )
    except Exception:
        _rag_instance = None
    return _rag_instance


async def search_curriculum(query: str, grade: Optional[str | int], subject: Optional[str] = None,
                            top_k: int = 3) -> Dict[str, Any]:
    """Async wrapper used from pipeline. Returns context/hits metadata."""
    rag = _get_rag_instance()
    if rag is None:
        return {"context": "", "hits": 0, "status": "unavailable", "reason": "rag_not_initialized"}

    if not rag.available:
        return {"context": "", "hits": 0, "status": "unavailable", "reason": "no_curriculum_data"}

    loop = asyncio.get_running_loop()
    results = await loop.run_in_executor(None, lambda: rag.query(query, grade=grade, subject=subject, top_k=top_k))

    if not results:
        return {"context": "", "hits": 0, "status": "no_matches"}

    context = rag.format_results(results)
    return {"context": context, "hits": len(results), "status": "ok"}
