"""RAG service implementation using ChromaDB and sentence-transformers."""

import logging
from typing import List, Dict, Any
import chromadb
from chromadb.config import Settings as ChromaSettings
from sentence_transformers import SentenceTransformer

from .config import settings

logger = logging.getLogger(__name__)


class RAGService:
    """Simple RAG service for document storage and retrieval."""
    
    def __init__(self):
        """Initialize the RAG service."""
        self.embedding_model = SentenceTransformer(settings.embedding_model)
        
        # Initialize ChromaDB client
        self.client = chromadb.PersistentClient(
            path=settings.chroma_persist_directory,
            settings=ChromaSettings(
                anonymized_telemetry=False,
                allow_reset=True,
            )
        )
        
        # Get or create collection
        self.collection = self.client.get_or_create_collection(
            name=settings.collection_name,
            metadata={"description": "RAG documents collection"}
        )
        
        logger.info("RAG service initialized successfully")
    
    def add_document(self, text: str, metadata: Dict[str, Any] = None) -> str:
        """
        Add a document to the RAG system.
        
        Args:
            text: Document text content
            metadata: Optional metadata for the document
            
        Returns:
            Document ID
        """
        if metadata is None:
            metadata = {}
        
        # Generate embedding
        embedding = self.embedding_model.encode(text).tolist()
        
        # Generate unique ID
        doc_id = f"doc_{self.collection.count() + 1}"
        
        # Add to collection
        self.collection.add(
            ids=[doc_id],
            embeddings=[embedding],
            documents=[text],
            metadatas=[metadata]
        )
        
        logger.info(f"Document added with ID: {doc_id}")
        return doc_id
    
    def query(self, query_text: str, top_k: int = None) -> List[Dict[str, Any]]:
        """
        Query the RAG system for relevant documents.
        
        Args:
            query_text: Query text
            top_k: Number of results to return
            
        Returns:
            List of relevant documents with metadata
        """
        if top_k is None:
            top_k = settings.top_k_results
        
        # Generate query embedding
        query_embedding = self.embedding_model.encode(query_text).tolist()
        
        # Query collection
        results = self.collection.query(
            query_embeddings=[query_embedding],
            n_results=top_k,
            include=["documents", "metadatas", "distances"]
        )
        
        # Format results
        formatted_results = []
        if results["documents"] and len(results["documents"][0]) > 0:
            for i, doc in enumerate(results["documents"][0]):
                formatted_results.append({
                    "id": results["ids"][0][i],
                    "text": doc,
                    "metadata": results["metadatas"][0][i],
                    "distance": results["distances"][0][i],
                })
        
        logger.info(f"Query returned {len(formatted_results)} results")
        return formatted_results
    
    def get_stats(self) -> Dict[str, Any]:
        """
        Get statistics about the RAG system.
        
        Returns:
            Statistics dictionary
        """
        return {
            "total_documents": self.collection.count(),
            "collection_name": settings.collection_name,
            "embedding_model": settings.embedding_model,
        }
    
    def delete_document(self, doc_id: str) -> bool:
        """
        Delete a document from the RAG system.
        
        Args:
            doc_id: Document ID to delete
            
        Returns:
            True if successful, False otherwise
        """
        try:
            self.collection.delete(ids=[doc_id])
            logger.info(f"Document deleted: {doc_id}")
            return True
        except Exception as e:
            logger.error(f"Error deleting document {doc_id}: {e}")
            return False
    
    def reset(self) -> bool:
        """
        Reset the RAG system (delete all documents).
        
        Returns:
            True if successful, False otherwise
        """
        try:
            self.client.delete_collection(name=settings.collection_name)
            self.collection = self.client.get_or_create_collection(
                name=settings.collection_name,
                metadata={"description": "RAG documents collection"}
            )
            logger.info("RAG system reset successfully")
            return True
        except Exception as e:
            logger.error(f"Error resetting RAG system: {e}")
            return False
