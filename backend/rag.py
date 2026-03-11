"""
RAG-modul. Placeholder för ChromaDB-integration.

Fas 2: Här ska Lgr22-data vektoriseras och sökas.
Just nu returnerar den tom kontext.
"""


async def search_curriculum(query: str, grade: int, subject: str = None) -> str:
    """
    Sök i lokal vektordatabas efter relevant kursplansinnehåll.

    TODO Fas 2:
    1. Installera chromadb
    2. Ladda Lgr22-data från Skolverkets API (JSON)
    3. Embeddda med Ollama (nomic-embed-text)
    4. Vid query: embed frågan, sök top-3, returnera som kontext

    Args:
        query: Barnets fråga
        grade: Årskurs (1-6)
        subject: Ämne (matematik, svenska, NO, etc)

    Returns:
        Kontextsträng att injicera i LLM-prompten, eller tom sträng.
    """
    return ""
