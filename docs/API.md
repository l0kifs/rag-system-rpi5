# API Documentation

Complete documentation for the RAG System API endpoints.

## Base URL

```
http://localhost:8000
```

## Interactive Documentation

The API includes auto-generated interactive documentation:

- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

## Endpoints

### Health Check

Check the health status of the API.

**Endpoint:** `GET /health`

**Response:**
```json
{
  "status": "healthy",
  "app_name": "RAG System RPi5",
  "version": "0.1.0"
}
```

**Example:**
```bash
curl http://localhost:8000/health
```

---

### Add Document

Add a new document to the RAG system.

**Endpoint:** `POST /documents`

**Request Body:**
```json
{
  "text": "string (required, min length: 1)",
  "metadata": {
    "key": "value"
  } // optional
}
```

**Response:**
```json
{
  "id": "doc_1",
  "message": "Document added successfully"
}
```

**Status Codes:**
- `201`: Document created successfully
- `422`: Validation error (invalid input)
- `500`: Internal server error

**Example:**
```bash
curl -X POST http://localhost:8000/documents \
  -H "Content-Type: application/json" \
  -d '{
    "text": "Python is a high-level programming language.",
    "metadata": {
      "topic": "programming",
      "author": "John Doe"
    }
  }'
```

---

### Query Documents

Search for relevant documents using semantic search.

**Endpoint:** `POST /query`

**Request Body:**
```json
{
  "query": "string (required, min length: 1)",
  "top_k": 5  // optional, default: 5, range: 1-20
}
```

**Response:**
```json
{
  "query": "What is Python?",
  "results": [
    {
      "id": "doc_1",
      "text": "Python is a high-level programming language.",
      "metadata": {
        "topic": "programming"
      },
      "distance": 0.234  // Lower is more similar
    }
  ],
  "count": 1
}
```

**Status Codes:**
- `200`: Success
- `422`: Validation error (invalid input)
- `500`: Internal server error

**Example:**
```bash
curl -X POST http://localhost:8000/query \
  -H "Content-Type: application/json" \
  -d '{
    "query": "Tell me about Python",
    "top_k": 3
  }'
```

---

### Get Statistics

Retrieve system statistics.

**Endpoint:** `GET /stats`

**Response:**
```json
{
  "total_documents": 10,
  "collection_name": "rag_documents",
  "embedding_model": "all-MiniLM-L6-v2"
}
```

**Status Codes:**
- `200`: Success
- `500`: Internal server error

**Example:**
```bash
curl http://localhost:8000/stats
```

---

### Delete Document

Delete a specific document by ID.

**Endpoint:** `DELETE /documents/{doc_id}`

**Path Parameters:**
- `doc_id` (string): The document ID to delete

**Response:**
```json
{
  "success": true,
  "message": "Document doc_1 deleted successfully"
}
```

**Status Codes:**
- `200`: Success
- `500`: Internal server error

**Example:**
```bash
curl -X DELETE http://localhost:8000/documents/doc_1
```

---

### Reset System

Delete all documents from the system.

**Endpoint:** `POST /reset`

**Response:**
```json
{
  "success": true,
  "message": "RAG system reset successfully"
}
```

**Status Codes:**
- `200`: Success
- `500`: Internal server error

**Example:**
```bash
curl -X POST http://localhost:8000/reset
```

---

## Error Handling

All errors return a consistent format:

```json
{
  "detail": "Error message describing what went wrong"
}
```

### Common Error Codes

- `400`: Bad Request - Invalid parameters
- `422`: Unprocessable Entity - Validation error
- `500`: Internal Server Error - Server-side error

## Rate Limiting

Currently, there are no rate limits. For production use, consider implementing rate limiting using:
- Nginx
- API Gateway
- Python rate limiting libraries

## CORS

CORS is enabled for all origins by default. To restrict in production, modify `main.py`:

```python
app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://yourdomain.com"],
    allow_credentials=True,
    allow_methods=["GET", "POST", "DELETE"],
    allow_headers=["*"],
)
```

## Authentication

The current implementation does not include authentication. For production use, consider adding:

1. **API Keys:**
   ```python
   from fastapi.security import APIKeyHeader
   
   api_key_header = APIKeyHeader(name="X-API-Key")
   ```

2. **OAuth2:**
   ```python
   from fastapi.security import OAuth2PasswordBearer
   
   oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")
   ```

3. **JWT Tokens:**
   ```python
   from jose import JWTError, jwt
   ```

## Best Practices

### Adding Documents

1. **Chunk Large Documents:**
   ```python
   # Instead of adding entire document
   # Break into smaller chunks
   chunks = split_text(large_document, chunk_size=500)
   for chunk in chunks:
       response = requests.post("/documents", json={"text": chunk})
   ```

2. **Use Meaningful Metadata:**
   ```python
   metadata = {
       "source": "user_manual.pdf",
       "page": 5,
       "section": "Installation",
       "created_at": "2024-01-01T00:00:00Z"
   }
   ```

### Querying

1. **Be Specific:**
   - Good: "What are the installation steps for Docker?"
   - Bad: "Docker"

2. **Use Top-K Wisely:**
   - Lower values (1-3) for precise answers
   - Higher values (5-10) for exploration

3. **Iterate on Queries:**
   - Refine based on results
   - Add context from metadata

### Performance

1. **Batch Operations:**
   ```python
   # Add multiple documents
   for doc in documents:
       requests.post("/documents", json=doc)
   ```

2. **Cache Results:**
   ```python
   # Client-side caching
   cache = {}
   if query in cache:
       return cache[query]
   result = requests.post("/query", json={"query": query})
   cache[query] = result.json()
   ```

## SDK Examples

### Python

```python
import requests

class RAGClient:
    def __init__(self, base_url="http://localhost:8000"):
        self.base_url = base_url
    
    def add_document(self, text, metadata=None):
        response = requests.post(
            f"{self.base_url}/documents",
            json={"text": text, "metadata": metadata}
        )
        return response.json()
    
    def query(self, query_text, top_k=5):
        response = requests.post(
            f"{self.base_url}/query",
            json={"query": query_text, "top_k": top_k}
        )
        return response.json()
    
    def get_stats(self):
        response = requests.get(f"{self.base_url}/stats")
        return response.json()

# Usage
client = RAGClient()
client.add_document("Python is awesome!")
results = client.query("Tell me about Python")
```

### JavaScript/Node.js

```javascript
class RAGClient {
  constructor(baseURL = 'http://localhost:8000') {
    this.baseURL = baseURL;
  }

  async addDocument(text, metadata = null) {
    const response = await fetch(`${this.baseURL}/documents`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ text, metadata })
    });
    return response.json();
  }

  async query(query, topK = 5) {
    const response = await fetch(`${this.baseURL}/query`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ query, top_k: topK })
    });
    return response.json();
  }

  async getStats() {
    const response = await fetch(`${this.baseURL}/stats`);
    return response.json();
  }
}

// Usage
const client = new RAGClient();
await client.addDocument('Python is awesome!');
const results = await client.query('Tell me about Python');
```

### cURL

See the examples provided in each endpoint section above.

## Monitoring

Track API usage and performance:

```bash
# Monitor response times
time curl http://localhost:8000/query -X POST \
  -H "Content-Type: application/json" \
  -d '{"query": "test"}'

# Check container logs
docker compose logs -f rag-app

# Monitor resource usage
docker stats rag-system-rpi5
```
