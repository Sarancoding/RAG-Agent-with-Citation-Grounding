from typing import List, Dict, Any

def format_citations(citations: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """
    Format citation objects for the final API response.
    """
    formatted = []
    for cit in citations:
        formatted.append({
            "source_id": cit.get("source_id", "unknown"),
            "text": cit.get("text", "")[:200] + "..." if len(cit.get("text", "")) > 200 else cit.get("text", ""),
            "page": cit.get("page")
        })
    return formatted
