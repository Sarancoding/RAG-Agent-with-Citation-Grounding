import os
from typing import List
from langchain_community.document_loaders import PyPDFLoader, TextLoader, Docx2txtLoader
from langchain_core.documents import Document

def load_document(file_path: str) -> List[Document]:
    """Load a document based on its extension."""
    ext = os.path.splitext(file_path)[1].lower()

    if ext == ".pdf":
        loader = PyPDFLoader(file_path)
    elif ext == ".txt":
        loader = TextLoader(file_path)
    elif ext == ".docx":
        loader = Docx2txtLoader(file_path)
    else:
        raise ValueError(f"Unsupported file format: {ext}")

    return loader.load()

def load_directory(directory_path: str) -> List[Document]:
    """Load all supported documents from a directory."""
    documents = []
    for root, _, files in os.walk(directory_path):
        for file in files:
            file_path = os.path.join(root, file)
            try:
                documents.extend(load_document(file_path))
            except ValueError:
                pass # Skip unsupported formats

    return documents
