# Working Guide

## Basic Query
```python
import requests

response = requests.post(
    "http://localhost:8000/api/query",
    json={
        "query": "What are the benefits of renewable energy?",
        "confidence_threshold": 70
    }
)
print(response.json())
```

## Expected Response
```json
{
  "answer": "Renewable energy reduces carbon emissions [Source 1] and provides energy independence [Source 2].",
  "citations": [
    {"source_id": "doc_001", "text": "...", "page": 5},
    {"source_id": "doc_003", "text": "...", "page": 12}
  ],
  "confidence_score": 85.3,
  "sources_used": 2,
  "fallback_triggered": false
}
```

## Low Confidence Handling
When confidence < threshold:
- Response includes warning flag
- System automatically triggers web search
- Combined answer shows both local and web sources

## Document Ingestion
```bash
python scripts/ingest_documents.py \
  --path /path/to/documents/ \
  --formats pdf,txt,docx \
  --chunk_size 500 \
  --overlap 50
```

## Monitoring
- Check logs: `tail -f logs/app.log`
- View metrics: http://localhost:8000/metrics
- Health check: http://localhost:8000/health
