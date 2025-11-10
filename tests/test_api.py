"""Test cases for the RAG API endpoints."""

import pytest
from fastapi.testclient import TestClient
from rag_system_rpi5.main import app


@pytest.fixture
def client():
    """Create a test client."""
    return TestClient(app)


def test_health_check(client):
    """Test the health check endpoint."""
    response = client.get("/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "healthy"
    assert "app_name" in data
    assert "version" in data


def test_root_endpoint(client):
    """Test the root endpoint."""
    response = client.get("/")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "healthy"


def test_add_document(client):
    """Test adding a document."""
    response = client.post(
        "/documents",
        json={
            "text": "Test document content",
            "metadata": {"test": "metadata"}
        }
    )
    assert response.status_code == 201
    data = response.json()
    assert "id" in data
    assert data["message"] == "Document added successfully"


def test_query_documents(client):
    """Test querying documents."""
    # First add a document
    client.post(
        "/documents",
        json={"text": "Python is a programming language"}
    )
    
    # Then query
    response = client.post(
        "/query",
        json={
            "query": "What is Python?",
            "top_k": 5
        }
    )
    assert response.status_code == 200
    data = response.json()
    assert "query" in data
    assert "results" in data
    assert "count" in data
    assert isinstance(data["results"], list)


def test_get_stats(client):
    """Test getting system statistics."""
    response = client.get("/stats")
    assert response.status_code == 200
    data = response.json()
    assert "total_documents" in data
    assert "collection_name" in data
    assert "embedding_model" in data


def test_invalid_document(client):
    """Test adding an invalid document."""
    response = client.post(
        "/documents",
        json={"text": ""}  # Empty text should fail validation
    )
    assert response.status_code == 422  # Validation error


def test_invalid_query(client):
    """Test querying with invalid parameters."""
    response = client.post(
        "/query",
        json={"query": "", "top_k": 5}  # Empty query should fail
    )
    assert response.status_code == 422  # Validation error
