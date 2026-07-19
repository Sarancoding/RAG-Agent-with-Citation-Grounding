import chromadb
from chromadb.config import Settings as ChromaSettings
from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_core.documents import Document
from typing import List, Tuple
from src.config import settings

class VectorStoreManager:
    """Manages the ChromaDB vector store."""
    def __init__(self, persist_directory: str = None):
        self.persist_directory = persist_directory or settings.vector_db_path
        self.embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
        self.vector_store = Chroma(
            persist_directory=self.persist_directory,
            embedding_function=self.embeddings,
            collection_name="rag_collection"
        )

    def add_documents(self, documents: List[Document]):
        """Add documents to the vector store."""
        self.vector_store.add_documents(documents)
        # ChromaDB automatically persists since recent versions,
        # but we can explicitly call persist if using an older version.
        try:
            self.vector_store.persist()
        except AttributeError:
            pass # persist is deprecated/removed in newer langchain-chroma

    def search(self, query: str, k: int = 4) -> List[Tuple[Document, float]]:
        """Search for relevant documents. Returns (Document, relevance_score)."""
        # similarity_search_with_relevance_scores returns scores (higher is better usually, depending on metric)
        results = self.vector_store.similarity_search_with_relevance_scores(query, k=k)
        return results

    def get_retriever(self, k: int = 4):
        """Get a retriever interface."""
        return self.vector_store.as_retriever(search_kwargs={"k": k})
