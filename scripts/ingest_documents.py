import argparse
import sys
import os

# Add the root directory to sys.path so we can import src
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.retrieval.document_loader import load_directory
from src.retrieval.vector_store import VectorStoreManager
from langchain_text_splitters import RecursiveCharacterTextSplitter

def main():
    parser = argparse.ArgumentParser(description="Ingest documents into the vector store.")
    parser.add_argument("--path", type=str, required=True, help="Path to the directory containing documents.")
    parser.add_argument("--chunk_size", type=int, default=500, help="Size of each document chunk.")
    parser.add_argument("--overlap", type=int, default=50, help="Overlap between document chunks.")

    args = parser.parse_args()

    print(f"Loading documents from {args.path}...")
    documents = load_directory(args.path)

    if not documents:
        print("No valid documents found.")
        return

    print(f"Loaded {len(documents)} documents. Splitting into chunks...")
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=args.chunk_size,
        chunk_overlap=args.overlap
    )
    chunks = text_splitter.split_documents(documents)

    print(f"Created {len(chunks)} chunks. Adding to vector store...")
    vsm = VectorStoreManager()
    vsm.add_documents(chunks)

    print("Ingestion complete!")

if __name__ == "__main__":
    main()
