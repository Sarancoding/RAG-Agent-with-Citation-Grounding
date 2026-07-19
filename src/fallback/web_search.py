from langchain_core.documents import Document
from duckduckgo_search import DDGS
from typing import List

def perform_web_search(query: str, max_results: int = 3) -> List[Document]:
    """
    Perform a web search as a fallback when local documents are insufficient.
    """
    try:
        with DDGS() as ddgs:
            results = list(ddgs.text(query, max_results=max_results))

        documents = []
        for res in results:
            doc = Document(
                page_content=res.get("body", ""),
                metadata={"source": res.get("href", "web_search"), "title": res.get("title", "")}
            )
            documents.append(doc)

        return documents
    except Exception as e:
        print(f"Web search failed: {e}")
        return []
