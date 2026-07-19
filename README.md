# RAG Agent with Citation Grounding
![Build Status](https://img.shields.io/badge/build-passing-brightgreen)
![License](https://img.shields.io/badge/license-MIT-blue)
![Python Version](https://img.shields.io/badge/python-3.10%2B-blue)

## Overview
A production-ready Retrieval-Augmented Generation (RAG) agent that retrieves context from knowledge sources, generates answers with verifiable citations, flags low-confidence responses, and implements fallback mechanisms to external search. The system prevents hallucinations at scale through citation grounding and confidence scoring.

## Features
* Retrieve relevant context from vector store based on user query
* Generate answers with inline citations [Source 1], [Source 2]
* Calculate and display confidence scores (0-100%)
* Flag responses below confidence threshold (<70%) with warnings
* Automatic fallback to web search when confidence is low or no relevant documents found
* Response validation against retrieved sources
* Support for multiple document formats (PDF, DOCX, TXT, HTML)
* RESTful API endpoints for integration
* Async processing for scalability

## Architecture Diagram
```
Client -> FastAPI Endpoint -> Confidence Scorer -> Generation Module (LLM) -> Citation Engine -> Response
         |                                           ^
         v                                           |
    Vector Store (Retrieval Module) -----------------+
         |
         v (fallback)
    Web Search (DuckDuckGo/SerpAPI)
```

## Quick Start
1. Clone the repository and run `pip install -r requirements.txt`.
2. Configure your environment variables in `.env`.
3. Run `uvicorn src.main:app --reload` to start the server.

For detailed setup, see [INSTALL.md](INSTALL.md).
For usage guide and API examples, see [USAGE.md](USAGE.md).

## Configuration
See `.env.example` for details on configuring environment variables.

## API Reference
The API documentation is available at `http://localhost:8000/docs` (Swagger UI) when the server is running.
- `POST /api/query`: Ask a question and get a response with citations.
- `GET /health`: Health check endpoint.
- `GET /metrics`: View application metrics.

## Testing
Run unit and integration tests using pytest:
```bash
pytest tests/ -v --cov=src
```

## Deployment
Docker deployment is supported via the included `Dockerfile` and `docker-compose.yml`.

## Performance Optimization
- Embeddings and vector similarity search use efficient models and libraries (e.g., ChromaDB, sentence-transformers).
- Async execution in FastAPI handles concurrent requests effectively.

## Troubleshooting
Check `logs/app.log` for detailed operation logs and errors. Make sure `.env` variables are correctly set (especially API keys).

## Contributing
Pull requests are welcome. Please ensure tests pass and follow code style guidelines.

## License
MIT License
