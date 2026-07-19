import pytest
from src.models.confidence import calculate_confidence_score

def test_calculate_confidence_score():
    scores = [0.8, 0.9]
    confidence = calculate_confidence_score(scores)
    # Average is 0.85 -> 85.0
    assert confidence == 85.0

def test_calculate_confidence_score_empty():
    assert calculate_confidence_score([]) == 0.0

def test_calculate_confidence_score_fallback():
    assert calculate_confidence_score([], fallback=True) == 50.0
