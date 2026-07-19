RAG_SYSTEM_PROMPT = """You are an expert answering questions based on the provided context.
Answer the question based ONLY on the provided context.
For each claim, cite the source using the exact [Source N] format.
If you cannot answer confidently from the context, state "LOW_CONFIDENCE".

Context provided will be in the format:
[Source 1] text snippet...
[Source 2] text snippet...

Ensure you map the [Source N] in your response back to the provided sources.
"""

def build_user_prompt(context_docs: list, query: str) -> str:
    """Build the user prompt with context and query."""
    context_str = ""
    for idx, doc in enumerate(context_docs, start=1):
        context_str += f"[Source {idx}] {doc.page_content}\n\n"

    prompt = f"Context:\n{context_str}\n\nQuestion: {query}\n\nAnswer with citations:"
    return prompt
