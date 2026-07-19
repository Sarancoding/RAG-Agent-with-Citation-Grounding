from typing import List, Dict, Any

def calculate_confidence_score(retrieval_scores: List[float], fallback: bool = False) -> float:
    """
    Calculate a confidence score (0-100%) based on retrieval similarity scores.
    If fallback is triggered, we set a default moderate confidence or calculate differently.
    """
    if fallback:
        return 50.0  # Default moderate confidence for web fallback if not explicitly scored

    if not retrieval_scores:
        return 0.0

    # Example logic: take the average of top scores and map to 0-100
    # Assuming retrieval_scores are cosine distances (0 to 1, where 0 is identical),
    # or similarities (0 to 1, where 1 is identical). We assume similarities.

    avg_score = sum(retrieval_scores) / len(retrieval_scores)
    # Ensure it's bounded between 0 and 100
    confidence = max(0.0, min(100.0, avg_score * 100.0))
    return round(confidence, 2)
