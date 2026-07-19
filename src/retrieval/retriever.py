from typing import List, Tuple, Dict, Any
from langchain_core.documents import Document
from src.retrieval.vector_store import VectorStoreManager

class SemanticRetriever:
    """Handles semantic search and score calculation."""
    def __init__(self, vector_store_manager: VectorStoreManager):
        self.vsm = vector_store_manager

    def retrieve(self, query: str, top_k: int = 4) -> Dict[str, Any]:
        """
        Retrieves top_k documents and returns a dictionary with
        documents, their scores, and average relevance.
        """
        results = self.vsm.search(query, k=top_k)

        documents = []
        scores = []

        for doc, score in results:
            documents.append(doc)
            scores.append(score)

        avg_score = sum(scores) / len(scores) if scores else 0.0

        return {
            "documents": documents,
            "scores": scores,
            "average_score": avg_score
        }
