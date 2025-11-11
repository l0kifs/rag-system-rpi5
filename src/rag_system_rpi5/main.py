"""FastAPI application for RAG system."""

import logging
from contextlib import asynccontextmanager
from fastapi import FastAPI, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware

from .config import settings
from .rag_service import RAGService
from .llm_service import LLMService
from .models import (
    DocumentCreate,
    DocumentResponse,
    QueryRequest,
    QueryResponse,
    QueryResult,
    StatsResponse,
    DeleteResponse,
    HealthResponse,
    ChatRequest,
    ChatResponse,
)

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

# Global service instances
rag_service: RAGService = None
llm_service: LLMService = None


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan manager."""
    global rag_service, llm_service
    
    # Startup
    logger.info("Starting RAG system...")
    rag_service = RAGService()
    logger.info("RAG system started successfully")
    
    logger.info("Starting LLM service...")
    try:
        llm_service = LLMService()
        # Optionally ensure model is available (can be slow on first run)
        # llm_service.ensure_model()
        logger.info("LLM service started successfully")
    except Exception as e:
        logger.warning(f"LLM service initialization failed: {e}")
        logger.warning("Chat endpoint will not be available")
    
    yield
    
    # Shutdown
    logger.info("Shutting down RAG system...")


# Create FastAPI application
app = FastAPI(
    title=settings.app_name,
    version=settings.app_version,
    description="Simple RAG (Retrieval-Augmented Generation) system for Raspberry Pi 5",
    lifespan=lifespan,
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/", response_model=HealthResponse)
async def root():
    """Root endpoint - health check."""
    return HealthResponse(
        status="healthy",
        app_name=settings.app_name,
        version=settings.app_version,
    )


@app.get("/health", response_model=HealthResponse)
async def health_check():
    """Health check endpoint."""
    return HealthResponse(
        status="healthy",
        app_name=settings.app_name,
        version=settings.app_version,
    )


@app.post("/documents", response_model=DocumentResponse, status_code=status.HTTP_201_CREATED)
async def add_document(document: DocumentCreate):
    """
    Add a new document to the RAG system.
    
    Args:
        document: Document data with text and optional metadata
        
    Returns:
        Document ID and success message
    """
    try:
        doc_id = rag_service.add_document(
            text=document.text,
            metadata=document.metadata
        )
        return DocumentResponse(
            id=doc_id,
            message="Document added successfully"
        )
    except Exception as e:
        logger.error(f"Error adding document: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error adding document: {str(e)}"
        )


@app.post("/query", response_model=QueryResponse)
async def query_documents(query_request: QueryRequest):
    """
    Query the RAG system for relevant documents.
    
    Args:
        query_request: Query text and optional parameters
        
    Returns:
        List of relevant documents
    """
    try:
        results = rag_service.query(
            query_text=query_request.query,
            top_k=query_request.top_k
        )
        
        query_results = [
            QueryResult(
                id=result["id"],
                text=result["text"],
                metadata=result["metadata"],
                distance=result["distance"]
            )
            for result in results
        ]
        
        return QueryResponse(
            query=query_request.query,
            results=query_results,
            count=len(query_results)
        )
    except Exception as e:
        logger.error(f"Error querying documents: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error querying documents: {str(e)}"
        )


@app.get("/stats", response_model=StatsResponse)
async def get_stats():
    """
    Get statistics about the RAG system.
    
    Returns:
        System statistics
    """
    try:
        stats = rag_service.get_stats()
        return StatsResponse(**stats)
    except Exception as e:
        logger.error(f"Error getting stats: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error getting stats: {str(e)}"
        )


@app.delete("/documents/{doc_id}", response_model=DeleteResponse)
async def delete_document(doc_id: str):
    """
    Delete a document from the RAG system.
    
    Args:
        doc_id: Document ID to delete
        
    Returns:
        Success status and message
    """
    try:
        success = rag_service.delete_document(doc_id)
        if success:
            return DeleteResponse(
                success=True,
                message=f"Document {doc_id} deleted successfully"
            )
        else:
            return DeleteResponse(
                success=False,
                message=f"Failed to delete document {doc_id}"
            )
    except Exception as e:
        logger.error(f"Error deleting document: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error deleting document: {str(e)}"
        )


@app.post("/reset", response_model=DeleteResponse)
async def reset_system():
    """
    Reset the RAG system (delete all documents).
    
    Returns:
        Success status and message
    """
    try:
        success = rag_service.reset()
        if success:
            return DeleteResponse(
                success=True,
                message="RAG system reset successfully"
            )
        else:
            return DeleteResponse(
                success=False,
                message="Failed to reset RAG system"
            )
    except Exception as e:
        logger.error(f"Error resetting system: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error resetting system: {str(e)}"
        )


@app.post("/chat", response_model=ChatResponse)
async def chat(chat_request: ChatRequest):
    """
    Chat with the LLM using RAG context.
    
    This endpoint retrieves relevant documents from the RAG system and uses them
    as context for the LLM to generate an informed response.
    
    Args:
        chat_request: Chat request with query and optional parameters
        
    Returns:
        LLM response with source documents
    """
    if llm_service is None:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="LLM service is not available. Please ensure Ollama is running and accessible."
        )
    
    try:
        # Retrieve relevant documents from RAG
        logger.info(f"Processing chat query: {chat_request.query[:50]}...")
        results = rag_service.query(
            query_text=chat_request.query,
            top_k=chat_request.top_k
        )
        
        # Generate response using LLM with context
        response_text = llm_service.generate_response(
            query=chat_request.query,
            context_documents=results,
            temperature=chat_request.temperature,
            max_tokens=chat_request.max_tokens
        )
        
        # Format source documents
        sources = [
            QueryResult(
                id=result["id"],
                text=result["text"],
                metadata=result["metadata"],
                distance=result["distance"]
            )
            for result in results
        ]
        
        return ChatResponse(
            query=chat_request.query,
            response=response_text,
            sources=sources,
            model=settings.ollama_model
        )
    except Exception as e:
        logger.error(f"Error processing chat request: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error processing chat request: {str(e)}"
        )


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
