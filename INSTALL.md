# Installation Guide

## Prerequisites
- Python 3.10+
- Docker & Docker Compose (optional, for containerized deployment)
- OpenAI API key or alternative LLM provider credentials
- SerpAPI key (for web search fallback)

## Step 1: Clone Repository
```bash
git clone https://github.com/yourusername/rag-citation-agent.git
cd rag-citation-agent
```

## Step 2: Setup Virtual Environment
```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
# or
venv\Scripts\activate     # Windows
```

## Step 3: Install Dependencies
```bash
pip install -r requirements.txt
```

## Step 4: Configure Environment Variables
```bash
cp .env.example .env
# Edit .env with your API keys:
# OPENAI_API_KEY=your_key_here
# SERPAPI_KEY=your_key_here
# CONFIDENCE_THRESHOLD=70
```

## Step 5: Ingest Sample Documents
```bash
python scripts/ingest_documents.py --path data/sample_documents/
```

## Step 6: Run Tests
```bash
pytest tests/ -v --cov=src
```

## Step 7: Start Application
```bash
uvicorn src.main:app --reload --host 0.0.0.0 --port 8000
```

## Verification
Visit http://localhost:8000/docs for Swagger UI
Test endpoint: curl http://localhost:8000/health
