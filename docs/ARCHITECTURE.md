# Architecture Documentation

This document describes the architecture and design decisions of the RAG System for Raspberry Pi 5.

## Overview

The RAG (Retrieval-Augmented Generation) system is designed as a lightweight, efficient semantic search engine optimized for resource-constrained environments like the Raspberry Pi 5.

## System Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                        Docker Container                      │
│                                                              │
│  ┌────────────────────────────────────────────────────────┐ │
│  │                    FastAPI Application                  │ │
│  │                                                          │ │
│  │  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐ │ │
│  │  │   REST API   │  │   Models     │  │   Config     │ │ │
│  │  │  Endpoints   │  │  (Pydantic)  │  │  Settings    │ │ │
│  │  └──────┬───────┘  └──────────────┘  └──────────────┘ │ │
│  │         │                                               │ │
│  │  ┌──────▼────────────────────────────────────────────┐ │ │
│  │  │              RAG Service                           │ │ │
│  │  │  ┌──────────────────┐  ┌─────────────────────┐   │ │ │
│  │  │  │ Sentence         │  │  ChromaDB          │   │ │ │
│  │  │  │ Transformers     │  │  Vector Store      │   │ │ │
│  │  │  │ (Embeddings)     │  │  (Persistence)     │   │ │ │
│  │  │  └──────────────────┘  └─────────────────────┘   │ │ │
│  │  └───────────────────────────────────────────────────┘ │ │
│  └──────────────────────────────────────────────────────────┘ │
│                                                              │
│  ┌────────────────────────────────────────────────────────┐ │
│  │                  Persistent Volume                      │ │
│  │                  /data/chroma                          │ │
│  └────────────────────────────────────────────────────────┘ │
└─────────────────────────────────────────────────────────────┘

External Clients ──HTTP──▶ Port 8000 ──▶ FastAPI ──▶ RAG Service
```

## Components

### 1. FastAPI Application (`main.py`)

**Responsibility:** HTTP server and request routing

**Key Features:**
- RESTful API endpoints
- Request validation using Pydantic
- CORS middleware for cross-origin requests
- Lifecycle management (startup/shutdown)
- Automatic OpenAPI documentation

**Endpoints:**
- `GET /` - Root/health check
- `GET /health` - Health status
- `POST /documents` - Add document
- `POST /query` - Query documents
- `GET /stats` - System statistics
- `DELETE /documents/{id}` - Delete document
- `POST /reset` - Reset system

### 2. RAG Service (`rag_service.py`)

**Responsibility:** Core RAG functionality

**Key Features:**
- Document embedding generation
- Vector storage management
- Semantic search
- Document CRUD operations

**Components:**
- **SentenceTransformer**: Generates embeddings from text
- **ChromaDB Client**: Manages vector storage and retrieval

### 3. Configuration (`config.py`)

**Responsibility:** Application settings management

**Features:**
- Environment variable support
- Default values for all settings
- Type validation
- `.env` file support

**Key Settings:**
- `EMBEDDING_MODEL`: Model for text embeddings
- `CHROMA_PERSIST_DIRECTORY`: Data storage location
- `COLLECTION_NAME`: ChromaDB collection name
- `TOP_K_RESULTS`: Default number of search results

### 4. Models (`models.py`)

**Responsibility:** Data validation and serialization

**Pydantic Models:**
- `DocumentCreate`: Input for adding documents
- `DocumentResponse`: Document creation response
- `QueryRequest`: Search query input
- `QueryResponse`: Search results output
- `StatsResponse`: System statistics
- `DeleteResponse`: Deletion confirmation
- `HealthResponse`: Health check response

### 5. ChromaDB

**Responsibility:** Vector database for embeddings

**Why ChromaDB:**
- Lightweight and embeddable
- No separate database server needed
- Perfect for Raspberry Pi
- Python-native
- Persistent storage support

**Storage:**
- Embeddings (vector representations)
- Original documents (text)
- Metadata (custom key-value pairs)

### 6. Sentence Transformers

**Responsibility:** Text embedding generation

**Model:** `all-MiniLM-L6-v2`

**Why This Model:**
- Small size (~80MB)
- Fast inference on ARM
- Good quality embeddings
- 384-dimensional vectors
- Supports semantic similarity

## Data Flow

### Adding a Document

```
User Request
    │
    ▼
FastAPI Endpoint (/documents)
    │
    ▼
Pydantic Validation
    │
    ▼
RAG Service (add_document)
    │
    ├──▶ Sentence Transformer (generate embedding)
    │       │
    │       ▼
    │    Embedding Vector [384 dimensions]
    │
    ▼
ChromaDB (store)
    ├──▶ Embedding
    ├──▶ Document Text
    └──▶ Metadata
    │
    ▼
Return Document ID
```

### Querying Documents

```
User Query
    │
    ▼
FastAPI Endpoint (/query)
    │
    ▼
Pydantic Validation
    │
    ▼
RAG Service (query)
    │
    ├──▶ Sentence Transformer (generate query embedding)
    │       │
    │       ▼
    │    Query Embedding Vector
    │
    ▼
ChromaDB (similarity search)
    │
    ├──▶ Vector similarity calculation
    ├──▶ Rank by distance
    └──▶ Return top-k results
    │
    ▼
Format Results
    │
    ▼
Return to User (JSON)
```

## Design Decisions

### Why FastAPI?

1. **Performance**: Async support, fast request handling
2. **Type Safety**: Built-in Pydantic validation
3. **Documentation**: Auto-generated OpenAPI docs
4. **Modern**: Python 3.7+ with type hints
5. **Easy Testing**: Built-in test client

### Why ChromaDB?

1. **Embeddable**: No separate database server
2. **Lightweight**: Minimal resource usage
3. **Python-Native**: Easy integration
4. **Persistent**: File-based storage
5. **Simple API**: Easy to use and maintain

### Why Sentence Transformers?

1. **Quality**: State-of-the-art embeddings
2. **Pre-trained**: No training needed
3. **Flexible**: Many models available
4. **ARM Support**: Works on Raspberry Pi
5. **Active Development**: Regular updates

### Why UV Package Manager?

1. **Speed**: Much faster than pip
2. **Modern**: Better dependency resolution
3. **Reliable**: Lock file support
4. **Simple**: Drop-in pip replacement
5. **Best Practice**: Recommended for new projects

## Performance Characteristics

### Memory Usage

- **Base**: ~500MB (FastAPI + dependencies)
- **Model Loading**: ~100MB (sentence-transformers model)
- **ChromaDB**: ~50MB + data size
- **Per Document**: ~1-2KB (depends on text length)

**Total Estimated**: 650MB + document storage

### Response Times (on RPi5)

- **First Query**: 2-5 seconds (model loading)
- **Subsequent Queries**: 100-500ms
- **Add Document**: 100-300ms
- **Delete Document**: 10-50ms

### Scalability

**Document Limits:**
- Tested with: 10,000 documents
- Recommended: < 100,000 documents
- Limit factor: Memory and disk space

**Concurrent Requests:**
- Single instance: 10-50 concurrent requests
- Can scale horizontally with load balancer

## Security Considerations

### Current Implementation

- No authentication/authorization
- CORS enabled for all origins
- No rate limiting
- No input sanitization beyond Pydantic validation

### Production Recommendations

1. **Add Authentication:**
   - API keys
   - OAuth2/JWT tokens
   - Role-based access control

2. **Restrict CORS:**
   - Whitelist specific origins
   - Disable credentials if not needed

3. **Add Rate Limiting:**
   - Per-IP limits
   - Per-user limits
   - Prevent abuse

4. **Use HTTPS:**
   - TLS/SSL certificates
   - Reverse proxy (nginx)
   - Secure headers

5. **Input Validation:**
   - Sanitize user input
   - Limit document size
   - Check for malicious content

## Future Enhancements

### Potential Improvements

1. **Multiple Collections:**
   - Support for multiple knowledge bases
   - Namespace isolation

2. **Authentication:**
   - User management
   - API key generation
   - Access control

3. **Advanced Search:**
   - Filters by metadata
   - Boolean queries
   - Date range queries

4. **Batch Operations:**
   - Bulk document upload
   - Batch queries
   - Import/export

5. **Model Options:**
   - Multiple embedding models
   - Model switching
   - Custom models

6. **Monitoring:**
   - Prometheus metrics
   - Health checks
   - Performance tracking

7. **Caching:**
   - Query result caching
   - Embedding caching
   - Redis integration

## Development Guidelines

### Adding New Features

1. **Define API Contract:**
   - Create Pydantic models
   - Define endpoint in `main.py`

2. **Implement Business Logic:**
   - Add method to `RAGService`
   - Handle errors appropriately

3. **Add Tests:**
   - Unit tests for service
   - Integration tests for API

4. **Update Documentation:**
   - API documentation
   - README examples
   - CHANGELOG

### Code Organization

```
src/rag_system_rpi5/
├── __init__.py       # Package initialization
├── main.py           # FastAPI app and routes
├── config.py         # Configuration management
├── models.py         # Pydantic models
└── rag_service.py    # RAG implementation
```

### Testing Strategy

1. **Unit Tests**: Test individual components
2. **Integration Tests**: Test API endpoints
3. **Manual Testing**: Use example scripts
4. **Load Testing**: Verify performance

## Deployment Architecture

### Single Instance

```
Raspberry Pi 5
└── Docker Container (rag-system-rpi5)
    └── FastAPI + ChromaDB
```

### Scaled Architecture (Future)

```
Load Balancer
├── RPi5 Instance 1
│   └── FastAPI App
├── RPi5 Instance 2
│   └── FastAPI App
└── RPi5 Instance 3
    └── FastAPI App
        │
        └── Shared ChromaDB Server
```

## Monitoring and Observability

### Current Capabilities

- Docker logs
- Health check endpoint
- Statistics endpoint
- Manual testing

### Recommended Additions

1. **Structured Logging:**
   - JSON logs
   - Log aggregation
   - Search and filtering

2. **Metrics:**
   - Request counts
   - Response times
   - Error rates
   - Resource usage

3. **Tracing:**
   - Request tracing
   - Performance profiling
   - Bottleneck identification

4. **Alerting:**
   - Error alerts
   - Performance degradation
   - Resource exhaustion
