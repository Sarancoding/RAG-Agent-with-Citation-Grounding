import re
from typing import List, Dict, Any

def parse_response(llm_output: str, source_mapping: Dict[int, Any]) -> Dict[str, Any]:
    """
    Parse the LLM output to extract citations.
    source_mapping maps an integer N to the actual Document metadata/object.
    """
    if "LOW_CONFIDENCE" in llm_output:
        return {
            "answer": llm_output,
            "citations": [],
            "low_confidence": True
        }

    # Extract all [Source N]
    citation_pattern = r"\[Source (\d+)\]"
    matches = re.findall(citation_pattern, llm_output)

    unique_sources = set(int(m) for m in matches)

    citations = []
    for source_num in unique_sources:
        if source_num in source_mapping:
            doc = source_mapping[source_num]
            citations.append({
                "source_id": doc.metadata.get("source", f"doc_{source_num}"),
                "text": doc.page_content,
                "page": doc.metadata.get("page", None)
            })

    return {
        "answer": llm_output,
        "citations": citations,
        "low_confidence": False
    }
