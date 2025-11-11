# LLM Integration Guide

This guide covers the integration of Ollama for local LLM inference in the RAG system, optimized for Raspberry Pi 5.

## Overview

The RAG system now includes an Ollama-powered LLM service that enables intelligent, context-aware responses to user queries. The system retrieves relevant documents from the vector database and uses them as context for the LLM to generate informed answers.

## Architecture

```
User Query
    │
    ├──> RAG Service (retrieves relevant documents)
    │         │
    │         └──> ChromaDB (vector search)
    │
    └──> LLM Service (generates response with context)
              │
              └──> Ollama (local LLM inference)
```

## Model Selection for Raspberry Pi 5

### Recommended Models

#### 1. qwen2.5:0.5b (Default)
- **Best for:** Quick responses, low memory usage
- **RAM Required:** ~500MB
- **Speed:** Fastest (near-instant responses)
- **Quality:** Good for simple queries
- **Use Case:** General purpose, resource-constrained environments

#### 2. phi3
- **Best for:** Better quality responses
- **RAM Required:** ~2GB
- **Speed:** Moderate
- **Quality:** Robust reasoning and understanding
- **Use Case:** When accuracy matters more than speed

#### 3. tinyllama
- **Best for:** Extremely fast responses
- **RAM Required:** ~400MB
- **Speed:** Very fast
- **Quality:** Basic
- **Use Case:** Simple queries, demos

### Switching Models

To change the model, update the `OLLAMA_MODEL` environment variable:

```bash
# In .env file
OLLAMA_MODEL=phi3

# Or in docker-compose.yml
environment:
  - OLLAMA_MODEL=phi3

# Then pull the new model
docker exec ollama ollama pull phi3

# Restart the rag-app container
docker-compose restart rag-app
```

## API Usage

### Chat Endpoint

The `/chat` endpoint combines RAG retrieval with LLM generation:

```bash
POST /chat
Content-Type: application/json

{
  "query": "string",           # Required: User's question
  "top_k": 3,                  # Optional: Number of context documents (1-10)
  "temperature": 0.7,          # Optional: LLM temperature (0.0-1.0)
  "max_tokens": 512            # Optional: Max response length (50-2048)
}
```

### Response Format

```json
{
  "query": "What is machine learning?",
  "response": "Machine learning is a subset of AI...",
  "sources": [
    {
      "id": "doc_1",
      "text": "Machine learning content...",
      "metadata": {"source": "ml_book.pdf"},
      "distance": 0.23
    }
  ],
  "model": "qwen2.5:0.5b"
}
```

### Example Workflow

```python
import requests

# 1. Add some documents
requests.post(
    "http://localhost:8000/documents",
    json={
        "text": "Machine learning is a subset of artificial intelligence.",
        "metadata": {"source": "ml_basics.txt"}
    }
)

# 2. Ask a question
response = requests.post(
    "http://localhost:8000/chat",
    json={
        "query": "What is machine learning?",
        "top_k": 3,
        "temperature": 0.7
    }
)

result = response.json()
print(f"Answer: {result['response']}")
print(f"\nSources used: {len(result['sources'])}")
for i, source in enumerate(result['sources'], 1):
    print(f"  {i}. {source['metadata'].get('source', 'Unknown')}")
```

## Configuration

### Environment Variables

```bash
# Ollama service endpoint
OLLAMA_HOST=http://localhost:11434

# LLM model to use
OLLAMA_MODEL=qwen2.5:0.5b

# Default generation temperature (0.0 = deterministic, 1.0 = creative)
OLLAMA_TEMPERATURE=0.7

# Default maximum tokens in response
OLLAMA_MAX_TOKENS=512
```

### Docker Compose Configuration

The Ollama service is defined in `docker-compose.yml`:

```yaml
services:
  ollama:
    image: ollama/ollama:latest
    container_name: ollama
    ports:
      - "11434:11434"
    volumes:
      - ollama-data:/root/.ollama
    environment:
      - OLLAMA_HOST=0.0.0.0
    restart: unless-stopped
```

## Performance Optimization

### Memory Management

1. **Model Selection:** Choose the smallest model that meets your needs
2. **Concurrent Requests:** Ollama handles one request at a time per model
3. **Context Size:** Limit `top_k` to reduce context size and improve speed

### Response Time Optimization

1. **Model Warm-up:** First request after container start is slower
2. **Reduce max_tokens:** Lower values = faster responses
3. **Temperature:** Lower temperature = more deterministic, slightly faster

### Best Practices

```python
# Fast, deterministic responses
response = requests.post("/chat", json={
    "query": "Quick question?",
    "top_k": 2,
    "temperature": 0.3,
    "max_tokens": 256
})

# High-quality, creative responses
response = requests.post("/chat", json={
    "query": "Complex question requiring analysis?",
    "top_k": 5,
    "temperature": 0.8,
    "max_tokens": 1024
})
```

## Troubleshooting

### Ollama Container Not Starting

```bash
# Check logs
docker-compose logs ollama

# Verify container is running
docker ps | grep ollama

# Restart Ollama
docker-compose restart ollama
```

### Model Not Found

```bash
# List available models
docker exec ollama ollama list

# Pull the required model
docker exec ollama ollama pull qwen2.5:0.5b

# If download is slow, it's normal for first time
# Models are 100MB-4GB depending on size
```

### Chat Endpoint Returns 503

This means the LLM service is unavailable. Check:

1. Is Ollama container running? `docker ps`
2. Is the model pulled? `docker exec ollama ollama list`
3. Can the rag-app reach Ollama? Check OLLAMA_HOST setting
4. Check logs: `docker-compose logs rag-app`

### Slow Responses

**First response is slow:** Normal - model needs to load into memory

**All responses are slow:**
- Consider using a smaller model (qwen2.5:0.5b or tinyllama)
- Reduce max_tokens
- Reduce top_k (fewer context documents)
- Check CPU/RAM usage: `docker stats`

### Out of Memory

```bash
# Use a smaller model
docker exec ollama ollama pull qwen2.5:0.5b

# Update .env
OLLAMA_MODEL=qwen2.5:0.5b

# Restart services
docker-compose restart
```

## Advanced Usage

### Custom Prompts

The LLM service builds prompts automatically, but you can influence the response:

```python
# Specific instruction in query
response = requests.post("/chat", json={
    "query": "List the top 3 key points about machine learning",
    "top_k": 5
})

# Request citations
response = requests.post("/chat", json={
    "query": "Explain neural networks and cite your sources",
    "top_k": 3
})
```

### Temperature Guidelines

- **0.0-0.3:** Deterministic, factual responses
- **0.4-0.7:** Balanced creativity and accuracy (default: 0.7)
- **0.8-1.0:** More creative, varied responses

### Token Guidelines

- **50-128:** Very short, concise answers
- **256-512:** Standard responses (default: 512)
- **512-1024:** Detailed explanations
- **1024-2048:** Comprehensive, in-depth responses

## Integration Examples

### Basic Q&A System

```python
def ask_question(question: str) -> str:
    """Simple Q&A function."""
    response = requests.post(
        "http://localhost:8000/chat",
        json={"query": question}
    )
    return response.json()["response"]

answer = ask_question("What is deep learning?")
print(answer)
```

### Interactive Chat with Context

```python
def chat_with_context(question: str, context_size: int = 3):
    """Chat with configurable context."""
    response = requests.post(
        "http://localhost:8000/chat",
        json={
            "query": question,
            "top_k": context_size,
            "temperature": 0.7
        }
    )
    
    result = response.json()
    
    print(f"Q: {result['query']}")
    print(f"A: {result['response']}")
    print(f"\nBased on {len(result['sources'])} documents:")
    for source in result['sources']:
        print(f"  - {source['metadata'].get('source', 'Unknown')}")
    
    return result

chat_with_context("How does machine learning work?")
```

### Batch Processing

```python
def process_questions(questions: list) -> list:
    """Process multiple questions."""
    results = []
    for question in questions:
        try:
            response = requests.post(
                "http://localhost:8000/chat",
                json={"query": question, "top_k": 3},
                timeout=30
            )
            results.append(response.json())
        except Exception as e:
            results.append({"error": str(e), "query": question})
    return results

questions = [
    "What is machine learning?",
    "What is deep learning?",
    "What are neural networks?"
]

answers = process_questions(questions)
for answer in answers:
    if "error" not in answer:
        print(f"Q: {answer['query']}")
        print(f"A: {answer['response']}\n")
```

## Security Considerations

1. **Local Only:** Ollama runs locally, data never leaves your system
2. **API Access:** Secure the API if exposed to network
3. **Model Trust:** Only use models from trusted sources
4. **Rate Limiting:** Consider adding rate limits for production use

## Monitoring

### Check Model Status

```bash
# List loaded models
docker exec ollama ollama list

# Check resource usage
docker stats ollama

# View logs
docker-compose logs -f ollama
```

### Performance Metrics

Monitor these metrics for production:
- Average response time per query
- Memory usage per model
- Request success rate
- Model load time

## References

- [Ollama Documentation](https://github.com/ollama/ollama)
- [Ollama Python Library](https://github.com/ollama/ollama-python)
- [RAG Best Practices](https://github.com/l0kifs/rag-system-rpi5/blob/main/docs/ARCHITECTURE.md)
