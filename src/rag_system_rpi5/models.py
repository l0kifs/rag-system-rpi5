"""Pydantic models for API requests and responses."""

from typing import Optional, List, Dict, Any
from pydantic import BaseModel, Field


class DocumentCreate(BaseModel):
    """Request model for creating a document."""
    
    text: str = Field(..., description="Document text content", min_length=1)
    metadata: Optional[Dict[str, Any]] = Field(default=None, description="Optional metadata")


class DocumentResponse(BaseModel):
    """Response model for document creation."""
    
    id: str = Field(..., description="Document ID")
    message: str = Field(..., description="Success message")


class QueryRequest(BaseModel):
    """Request model for querying documents."""
    
    query: str = Field(..., description="Query text", min_length=1)
    top_k: Optional[int] = Field(default=5, description="Number of results to return", ge=1, le=20)


class QueryResult(BaseModel):
    """Individual query result."""
    
    id: str = Field(..., description="Document ID")
    text: str = Field(..., description="Document text")
    metadata: Dict[str, Any] = Field(..., description="Document metadata")
    distance: float = Field(..., description="Distance/similarity score")


class QueryResponse(BaseModel):
    """Response model for query results."""
    
    query: str = Field(..., description="Original query text")
    results: List[QueryResult] = Field(..., description="Query results")
    count: int = Field(..., description="Number of results returned")


class StatsResponse(BaseModel):
    """Response model for system statistics."""
    
    total_documents: int = Field(..., description="Total number of documents")
    collection_name: str = Field(..., description="Collection name")
    embedding_model: str = Field(..., description="Embedding model name")


class DeleteResponse(BaseModel):
    """Response model for document deletion."""
    
    success: bool = Field(..., description="Whether deletion was successful")
    message: str = Field(..., description="Status message")


class HealthResponse(BaseModel):
    """Response model for health check."""
    
    status: str = Field(..., description="Health status")
    app_name: str = Field(..., description="Application name")
    version: str = Field(..., description="Application version")


class ChatRequest(BaseModel):
    """Request model for chat with LLM."""
    
    query: str = Field(..., description="User's question or query", min_length=1)
    top_k: Optional[int] = Field(default=3, description="Number of context documents to retrieve", ge=1, le=10)
    temperature: Optional[float] = Field(default=None, description="LLM temperature (0.0-1.0)", ge=0.0, le=1.0)
    max_tokens: Optional[int] = Field(default=None, description="Maximum tokens in response", ge=50, le=2048)


class ChatResponse(BaseModel):
    """Response model for chat."""
    
    query: str = Field(..., description="Original query")
    response: str = Field(..., description="LLM generated response")
    sources: List[QueryResult] = Field(..., description="Source documents used for context")
    model: str = Field(..., description="LLM model used")
