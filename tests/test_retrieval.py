import pytest
import os
from langchain_core.documents import Document
from src.retrieval.document_loader import load_document
from src.retrieval.vector_store import VectorStoreManager
from src.retrieval.retriever import SemanticRetriever

def test_load_document(tmp_path):
    # Test txt loader
    test_file = tmp_path / "test.txt"
    test_file.write_text("Hello World!")

    docs = load_document(str(test_file))
    assert len(docs) == 1
    assert "Hello World!" in docs[0].page_content

def test_vector_store(tmp_path):
    vsm = VectorStoreManager(persist_directory=str(tmp_path))
    docs = [Document(page_content="Test document content.", metadata={"source": "test.txt"})]
    vsm.add_documents(docs)

    results = vsm.search("Test", k=1)
    assert len(results) == 1
    assert "Test document content." in results[0][0].page_content

def test_retriever(tmp_path):
    vsm = VectorStoreManager(persist_directory=str(tmp_path))
    docs = [Document(page_content="Semantic retriever test content.", metadata={"source": "test.txt"})]
    vsm.add_documents(docs)

    retriever = SemanticRetriever(vsm)
    result = retriever.retrieve("Semantic", top_k=1)

    assert "documents" in result
    assert "scores" in result
    assert "average_score" in result
    assert len(result["documents"]) == 1
