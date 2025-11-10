# Examples

This directory contains example scripts demonstrating how to use the RAG system API.

## test_api.py

A comprehensive example that demonstrates all API endpoints:

- Adding documents to the RAG system
- Querying for relevant documents
- Getting system statistics
- Deleting documents

### Usage

1. Make sure the RAG system is running:
   ```bash
   docker compose up -d
   ```

2. Run the example script:
   ```bash
   python examples/test_api.py
   ```

   Or directly:
   ```bash
   ./examples/test_api.py
   ```

### Expected Output

The script will:
1. Check the API health
2. Add 5 sample documents
3. Show system statistics
4. Run 4 different queries
5. Delete one document
6. Show final statistics

You should see detailed output for each operation, including response codes and JSON responses.

## chat_example.py (NEW!)

A complete example demonstrating the new LLM-powered chat functionality:

- Adding documents about machine learning, deep learning, Python, and neural networks
- Using the `/chat` endpoint to get intelligent, context-aware responses
- Comparing traditional RAG queries with LLM-powered responses
- Different chat parameters (temperature, max_tokens, top_k)

### Prerequisites

1. Ensure Ollama container is running:
   ```bash
   docker compose up -d
   ```

2. Install the LLM model (first time only):
   ```bash
   ./scripts/install_model.sh
   # Or manually:
   docker exec ollama ollama pull qwen2.5:0.5b
   ```

### Usage

```bash
python examples/chat_example.py
```

Or directly:
```bash
./examples/chat_example.py
```

### Expected Output

The script will:
1. Check API availability
2. Add 4 sample documents about AI/ML topics
3. Run 4 different chat examples:
   - Simple question about machine learning
   - Comparative question (ML vs. Deep Learning)
   - Specific question about Python
   - Comparison of traditional RAG vs. LLM-powered chat
4. Show formatted responses with sources

### Example Questions You Can Try

After running the example, try these with curl:

```bash
# Simple factual question
curl -X POST http://localhost:8000/chat \
  -H "Content-Type: application/json" \
  -d '{"query": "What is deep learning?", "top_k": 2}'

# Comparison question
curl -X POST http://localhost:8000/chat \
  -H "Content-Type: application/json" \
  -d '{"query": "Compare machine learning and deep learning", "top_k": 3}'

# Creative response (higher temperature)
curl -X POST http://localhost:8000/chat \
  -H "Content-Type: application/json" \
  -d '{"query": "Explain neural networks in simple terms", "temperature": 0.8}'

# Deterministic response (lower temperature)
curl -X POST http://localhost:8000/chat \
  -H "Content-Type: application/json" \
  -d '{"query": "List key features of Python for ML", "temperature": 0.3}'
```
