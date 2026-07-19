from pydantic import BaseModel, Field
from typing import List, Optional

class QueryRequest(BaseModel):
    """Request model for querying the RAG agent."""
    query: str = Field(..., description="The user's query.")
    confidence_threshold: Optional[float] = Field(None, description="Optional override for the confidence threshold.")

class Citation(BaseModel):
    """Model representing a citation."""
    source_id: str = Field(..., description="The ID of the source document.")
    text: str = Field(..., description="The text snippet from the source.")
    page: Optional[int] = Field(None, description="The page number, if applicable.")

class QueryResponse(BaseModel):
    """Response model for a query."""
    answer: str = Field(..., description="The generated answer with inline citations.")
    citations: List[Citation] = Field(default_factory=list, description="List of citations used in the answer.")
    confidence_score: float = Field(..., description="The confidence score of the answer.")
    sources_used: int = Field(..., description="Number of sources used.")
    fallback_triggered: bool = Field(False, description="Whether web search fallback was triggered.")
