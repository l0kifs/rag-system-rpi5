# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.1.0] - 2024-01-10

### Added

#### Core Features
- FastAPI-based REST API for document management and semantic search
- ChromaDB integration for vector storage and retrieval
- Sentence-transformers for text embeddings (using all-MiniLM-L6-v2 model)
- Docker Compose setup for easy deployment
- UV package manager integration
- Pydantic models for request/response validation
- Environment-based configuration management

#### API Endpoints
- `GET /` - Root endpoint with health status
- `GET /health` - Detailed health check
- `POST /documents` - Add documents with optional metadata
- `POST /query` - Semantic search with configurable top-k results
- `GET /stats` - System statistics (document count, model info)
- `DELETE /documents/{id}` - Delete specific documents
- `POST /reset` - Reset the entire system

#### Documentation
- Comprehensive README with quick start guide
- API documentation with examples for all endpoints
- Deployment guide for Raspberry Pi 5 and cloud platforms
- Architecture documentation explaining design decisions
- Contributing guidelines with best practices
- Example scripts demonstrating API usage

#### Tools & Scripts
- Makefile with common commands (up, down, logs, test, etc.)
- Python example script for testing all API features
- Health check shell script for monitoring
- Docker and docker-compose configurations
- Environment file template

#### Testing
- Pytest-based test suite
- API endpoint tests
- Test fixtures for isolated testing
- Temporary ChromaDB directory for tests

#### Best Practices
- Type hints throughout the codebase
- CORS middleware for cross-origin requests
- Async/await support with FastAPI
- Proper error handling and logging
- Health checks in Docker Compose
- Volume persistence for data
- Security considerations documented

### Optimizations
- Lightweight embedding model optimized for ARM architecture
- Minimal Docker image using Python slim base
- Efficient vector storage with ChromaDB
- Resource-conscious design for Raspberry Pi 5

### Security
- CodeQL security scanning passed with zero alerts
- Input validation using Pydantic
- Structured error responses
- Security best practices documented for production use

## [Unreleased]

### Planned Features
- Multiple collection support
- User authentication and authorization
- Advanced search filters (metadata-based)
- Batch operations for documents
- Query result caching
- Additional embedding model options
- Prometheus metrics integration
- Rate limiting
- API versioning

### Under Consideration
- Web UI for document management
- CLI tool for system administration
- Database migration tools
- Integration with popular LLM APIs
- Document preprocessing pipelines
- Multi-language support
- Export/import functionality

---

[0.1.0]: https://github.com/l0kifs/rag-system-rpi5/releases/tag/v0.1.0
