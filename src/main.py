from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded
import time

from src.models.schemas import QueryRequest, QueryResponse
from src.retrieval.vector_store import VectorStoreManager
from src.retrieval.retriever import SemanticRetriever
from src.generation.llm_client import LLMClient
from src.generation.prompt_templates import RAG_SYSTEM_PROMPT, build_user_prompt
from src.generation.response_parser import parse_response
from src.citation.formatter import format_citations
from src.models.confidence import calculate_confidence_score
from src.fallback.web_search import perform_web_search
from src.monitoring.logger import logger
from src.monitoring.metrics import metrics_collector
from src.config import settings

app = FastAPI(title="RAG Citation Agent", version="1.0.0")

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins, adjust in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Setup Rate Limiter
limiter = Limiter(key_func=get_remote_address)
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

vsm = VectorStoreManager()
retriever = SemanticRetriever(vsm)
llm_client = LLMClient()

@app.get("/health")
@limiter.limit("5/minute")
async def health_check(request: Request):
    """Health check endpoint."""
    return {"status": "healthy"}

@app.get("/metrics")
@limiter.limit("10/minute")
async def metrics(request: Request):
    """Metrics endpoint."""
    return metrics_collector.get_metrics()

@app.post("/api/query", response_model=QueryResponse)
@limiter.limit("10/minute")
async def query_agent(request: Request, body: QueryRequest):
    """Main query endpoint."""
    start_time = time.time()
    fallback_triggered = False

    threshold = body.confidence_threshold if body.confidence_threshold is not None else settings.confidence_threshold

    try:
        # 1. Retrieve documents
        retrieval_result = retriever.retrieve(body.query)
        documents = retrieval_result["documents"]
        scores = retrieval_result["scores"]

        confidence = calculate_confidence_score(scores)

        # 2. Check fallback condition
        if confidence < threshold or not documents:
            logger.info(f"Low confidence ({confidence}) or no documents. Triggering fallback.")
            fallback_triggered = True
            documents = perform_web_search(body.query)
            # Assign fake scores for web documents or recalibrate confidence
            scores = [0.5] * len(documents)
            confidence = calculate_confidence_score(scores, fallback=True)

        if not documents:
            raise HTTPException(status_code=404, detail="No relevant information found.")

        # Create mapping for parsing
        source_mapping = {idx: doc for idx, doc in enumerate(documents, start=1)}

        # 3. Generate Answer
        user_prompt = build_user_prompt(documents, body.query)
        llm_output = await llm_client.generate_response(RAG_SYSTEM_PROMPT, user_prompt)

        # 4. Parse Response & Extract Citations
        parsed = parse_response(llm_output, source_mapping)
        citations = format_citations(parsed["citations"])

        # 5. Record Metrics
        process_time = time.time() - start_time
        metrics_collector.record_query(process_time, fallback_triggered)

        # 6. Return Response
        return QueryResponse(
            answer=parsed["answer"],
            citations=citations,
            confidence_score=confidence,
            sources_used=len(citations),
            fallback_triggered=fallback_triggered
        )

    except Exception as e:
        logger.error(f"Error processing query: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal server error")
