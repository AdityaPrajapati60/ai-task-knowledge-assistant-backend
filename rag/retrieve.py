import os
import re
from rag.vector_store import get_vector_store
from groq import Groq
from rank_bm25 import BM25Okapi  # NEW

client = Groq()

RERANKING_ENABLED = os.getenv("RERANKING_ENABLED", "true").lower() == "true"

# ---------------------------------------------------
# BM25 SEARCH (Keyword search)
# ---------------------------------------------------
def bm25_search(query, docs, top_k=5):
    corpus = [d.page_content.split() for d in docs]
    bm25 = BM25Okapi(corpus)
    scores = bm25.get_scores(query.split())

    scored = list(zip(docs, scores))
    scored.sort(key=lambda x: x[1], reverse=True)
    return [doc for doc, _ in scored[:top_k]]


# ---------------------------------------------------
# LLM RERANKER
# ---------------------------------------------------
def rerank_with_llm(query, docs, top_k=5):
    docs = [d for d in docs if d.page_content.strip()]
    if not docs:
        return []

    trimmed = [d.page_content[:400] for d in docs]

    prompt = f"""
Rank the chunks by relevance to the question.
Return ONLY comma-separated chunk numbers.

Question: {query}
""" + "\n\n".join([f"{i+1}. {c}" for i, c in enumerate(trimmed)])

    response = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[{"role": "user", "content": prompt}],
        temperature=0,
    )

    numbers = re.findall(r"\d+", response.choices[0].message.content)
    order = [int(n) - 1 for n in numbers if 0 < int(n) <= len(docs)]

    seen = set()
    ranked_docs = []
    for idx in order:
        if idx not in seen:
            ranked_docs.append(docs[idx])
            seen.add(idx)

    return ranked_docs[:top_k] if ranked_docs else docs[:top_k]


# ---------------------------------------------------
# MAIN RETRIEVE FUNCTION (HYBRID)
# ---------------------------------------------------
def retrieve_context(query: str, user_id: int, k: int = 20) -> str | None:
    vector_store = get_vector_store(user_id)

    # Step 1: Vector retrieval
    vector_docs = vector_store.similarity_search(query, k=k)
    if not vector_docs:
        return None

    # Step 2: BM25 keyword ranking on those docs
    bm25_docs = bm25_search(query, vector_docs, top_k=5)

    # Step 3: Merge vector + BM25 (unique)
    seen = set()
    hybrid_docs = []
    for d in vector_docs + bm25_docs:
        if d.page_content not in seen:
            hybrid_docs.append(d)
            seen.add(d.page_content)

    # Step 4: Optional LLM rerank
    if RERANKING_ENABLED:
        final_docs = rerank_with_llm(query, hybrid_docs, top_k=5)
    else:
        final_docs = hybrid_docs[:5]

    # Return context string
    return "\n\n".join(d.page_content for d in final_docs)
