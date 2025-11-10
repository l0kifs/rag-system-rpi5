# RAG System for Raspberry Pi 5

A simple and efficient Retrieval-Augmented Generation (RAG) system optimized for Raspberry Pi 5, built with FastAPI, ChromaDB, Ollama, and sentence-transformers.

## Features

- 🚀 **FastAPI** - Modern, fast web framework for building APIs
- 📦 **UV Package Manager** - Fast Python package management
- 🐳 **Docker Compose** - Easy deployment with containerization
- 🔍 **ChromaDB** - Lightweight vector database for document storage
- 🧠 **Sentence Transformers** - Efficient text embeddings optimized for ARM
- 🤖 **Ollama** - Local LLM inference for intelligent responses
- 🔌 **RESTful API** - Simple HTTP endpoints for document management and querying

## Architecture

```
┌─────────────────────────────────────┐
│         FastAPI App                 │
│                                     │
│  ┌───────────┐       ┌───────────┐ │
│  │ REST API  │───────│   LLM     │ │
│  └─────┬─────┘       │  Service  │ │
│        │             └─────┬─────┘ │
│  ┌─────▼─────┐             │       │
│  │   RAG     │             │       │
│  │  Service  │             │       │
│  └─────┬─────┘             │       │
│        │                   │       │
│  ┌─────▼─────┐       ┌─────▼─────┐ │
│  │ ChromaDB  │       │  Ollama   │ │
│  └───────────┘       └───────────┘ │
└─────────────────────────────────────┘
```

## Prerequisites

- Raspberry Pi 5 (or any ARM64/x86_64 system)
- Docker and Docker Compose installed
- At least 4GB of RAM (8GB recommended for LLM)
- At least 4GB of free disk space (for models)

## Quick Start

### Using Docker Compose (Recommended)

1. **Clone the repository:**
   ```bash
   git clone https://github.com/l0kifs/rag-system-rpi5.git
   cd rag-system-rpi5
   ```

2. **Start the application:**
   ```bash
   docker-compose up -d
   ```

3. **Install the LLM model (first time only):**
   ```bash
   # Option 1: Use the installation script (recommended)
   ./scripts/install_model.sh
   
   # Option 2: Manual installation
   docker exec ollama ollama pull qwen2.5:0.5b
   ```
   
   Alternative models for RPi5:
   - `phi3` - Better quality, slightly slower
   - `tinyllama` - Fastest, basic quality
   
   To install a different model:
   ```bash
   ./scripts/install_model.sh phi3
   ```

4. **Check the logs:**
   ```bash
   docker-compose logs -f
   ```

5. **Access the API:**
   - API Documentation: http://localhost:8000/docs
   - Health Check: http://localhost:8000/health
   - Ollama API: http://localhost:11434

### Local Development

1. **Install UV package manager:**
   ```bash
   curl -LsSf https://astral.sh/uv/install.sh | sh
   ```

2. **Install dependencies:**
   ```bash
   uv pip install -e .
   ```

3. **Run the application:**
   ```bash
   uvicorn rag_system_rpi5.main:app --reload
   ```

## API Endpoints

### Health Check
```bash
GET /health
```

### Add Document
```bash
POST /documents
Content-Type: application/json

{
  "text": "Your document content here",
  "metadata": {
    "source": "example.txt",
    "author": "John Doe"
  }
}
```

### Query Documents
```bash
POST /query
Content-Type: application/json

{
  "query": "What is machine learning?",
  "top_k": 5
}
```

### Chat with LLM (New!)
```bash
POST /chat
Content-Type: application/json

{
  "query": "What is machine learning?",
  "top_k": 3,
  "temperature": 0.7,
  "max_tokens": 512
}
```

### Get Statistics
```bash
GET /stats
```

### Delete Document
```bash
DELETE /documents/{doc_id}
```

### Reset System
```bash
POST /reset
```

## Usage Examples

### Using cURL

**Add a document:**
```bash
curl -X POST http://localhost:8000/documents \
  -H "Content-Type: application/json" \
  -d '{
    "text": "Machine learning is a subset of artificial intelligence that focuses on building systems that learn from data.",
    "metadata": {"topic": "AI", "category": "definition"}
  }'
```

**Query documents:**
```bash
curl -X POST http://localhost:8000/query \
  -H "Content-Type: application/json" \
  -d '{
    "query": "What is machine learning?",
    "top_k": 3
  }'
```

**Get system statistics:**
```bash
curl http://localhost:8000/stats
```

**Chat with LLM:**
```bash
curl -X POST http://localhost:8000/chat \
  -H "Content-Type: application/json" \
  -d '{
    "query": "What is machine learning?",
    "top_k": 3,
    "temperature": 0.7
  }'
```

### Using Python

```python
import requests

# Add document
response = requests.post(
    "http://localhost:8000/documents",
    json={
        "text": "Python is a high-level programming language.",
        "metadata": {"topic": "programming"}
    }
)
print(response.json())

# Query
response = requests.post(
    "http://localhost:8000/query",
    json={
        "query": "Tell me about Python",
        "top_k": 5
    }
)
print(response.json())

# Chat with LLM
response = requests.post(
    "http://localhost:8000/chat",
    json={
        "query": "Explain Python based on the documents",
        "top_k": 3
    }
)
print(response.json())
```

## Configuration

Configuration can be set via environment variables or `.env` file:

```bash
# ChromaDB settings
CHROMA_PERSIST_DIRECTORY=/data/chroma
COLLECTION_NAME=rag_documents

# Embedding model (optimized for ARM)
EMBEDDING_MODEL=all-MiniLM-L6-v2

# Ollama LLM settings
OLLAMA_HOST=http://localhost:11434
OLLAMA_MODEL=qwen2.5:0.5b
OLLAMA_TEMPERATURE=0.7
OLLAMA_MAX_TOKENS=512

# API settings
MAX_UPLOAD_SIZE=10485760
TOP_K_RESULTS=5
```

## Docker Commands

**Start services:**
```bash
docker-compose up -d
```

**Stop services:**
```bash
docker-compose down
```

**View logs:**
```bash
docker-compose logs -f rag-app
```

**Rebuild after changes:**
```bash
docker-compose up -d --build
```

**Remove all data:**
```bash
docker-compose down -v
```

## Performance Tips for Raspberry Pi 5

### LLM Model Selection
- **qwen2.5:0.5b** (Default) - Fastest, lowest RAM (~500MB), best for quick responses
- **phi3** - Better quality, moderate speed, uses ~2GB RAM
- **tinyllama** - Very fast, basic quality, ~400MB RAM

### General Tips
1. **Memory Management:** The system uses `all-MiniLM-L6-v2` embedding model which is lightweight and optimized for embedded systems
2. **LLM Performance:** First LLM inference will be slower as the model loads. Subsequent queries are faster
3. **Persistent Storage:** Data is stored in Docker volumes, ensuring persistence across restarts
4. **Resource Limits:** Consider setting memory limits in docker-compose.yml for production use
5. **Model Caching:** Both embedding and LLM models are cached after first load
6. **Cooling:** Use active cooling (fan/heatsink) for sustained AI workloads

## Troubleshooting

**Issue: Container fails to start**
- Check logs: `docker-compose logs rag-app` or `docker-compose logs ollama`
- Ensure sufficient memory is available (4GB+ recommended)
- Verify Docker and Docker Compose versions

**Issue: Chat endpoint returns 503**
- Ensure Ollama container is running: `docker ps`
- Check Ollama logs: `docker-compose logs ollama`
- Verify model is pulled: `docker exec ollama ollama list`
- Pull model manually: `docker exec ollama ollama pull qwen2.5:0.5b`

**Issue: Slow embedding generation**
- This is normal on first run as the model needs to be downloaded
- Subsequent runs will be faster due to caching

**Issue: Slow LLM responses**
- First response after model load is slower (model initialization)
- Use a smaller model like `qwen2.5:0.5b` or `tinyllama`
- Reduce `max_tokens` in chat requests
- Reduce `top_k` to retrieve fewer context documents

**Issue: Out of memory errors**
- Reduce `TOP_K_RESULTS` in configuration
- Use a smaller LLM model
- Use a smaller embedding model
- Increase swap space on Raspberry Pi

## Development

**Run tests:**
```bash
uv run pytest
```

**Format code:**
```bash
uv run ruff check --fix src/
```

## Project Structure

```
rag-system-rpi5/
├── src/
│   └── rag_system_rpi5/
│       ├── __init__.py
│       ├── main.py          # FastAPI application
│       ├── config.py        # Configuration management
│       ├── models.py        # Pydantic models
│       └── rag_service.py   # RAG implementation
├── Dockerfile               # Docker image definition
├── docker-compose.yml       # Docker Compose configuration
├── pyproject.toml          # Project dependencies (UV)
├── .env.example            # Example environment variables
└── README.md               # This file
```

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## Acknowledgments

- FastAPI for the excellent web framework
- ChromaDB for the vector database
- Sentence Transformers for the embedding models
- UV for fast Python package management
