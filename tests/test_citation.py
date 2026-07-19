import pytest
from src.citation.formatter import format_citations
from src.citation.grounding import verify_citations

def test_format_citations():
    raw_citations = [
        {"source_id": "doc1", "text": "A" * 250, "page": 1}
    ]

    formatted = format_citations(raw_citations)

    assert len(formatted) == 1
    assert formatted[0]["source_id"] == "doc1"
    assert formatted[0]["page"] == 1
    # Check truncation
    assert len(formatted[0]["text"]) == 203 # 200 chars + "..."

def test_verify_citations():
    # Currently a stub
    assert verify_citations("answer", [{"source_id": "1"}]) == True
