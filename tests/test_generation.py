import pytest
from src.generation.prompt_templates import build_user_prompt
from langchain_core.documents import Document
from src.generation.response_parser import parse_response

def test_build_user_prompt():
    docs = [Document(page_content="Content 1")]
    prompt = build_user_prompt(docs, "What is it?")
    assert "[Source 1] Content 1" in prompt
    assert "Question: What is it?" in prompt

def test_parse_response():
    llm_output = "The answer is 42 [Source 1]."
    mapping = {1: Document(page_content="Content 1", metadata={"source": "doc1"})}

    parsed = parse_response(llm_output, mapping)

    assert parsed["answer"] == llm_output
    assert len(parsed["citations"]) == 1
    assert parsed["citations"][0]["source_id"] == "doc1"
    assert parsed["low_confidence"] == False

def test_parse_response_low_confidence():
    llm_output = "LOW_CONFIDENCE: I don't know."
    mapping = {}

    parsed = parse_response(llm_output, mapping)
    assert parsed["low_confidence"] == True
