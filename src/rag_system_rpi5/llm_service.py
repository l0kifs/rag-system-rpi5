"""LLM service implementation using Ollama."""

import logging
from typing import List, Dict, Any, Optional
import ollama

from .config import settings

logger = logging.getLogger(__name__)


class LLMService:
    """Service for LLM interactions via Ollama."""
    
    def __init__(self):
        """Initialize the LLM service."""
        self.client = ollama.Client(host=settings.ollama_host)
        self.model = settings.ollama_model
        logger.info(f"LLM service initialized with model: {self.model}")
    
    def ensure_model(self) -> bool:
        """
        Ensure the model is available, pull if necessary.
        
        Returns:
            True if model is available, False otherwise
        """
        try:
            models = self.client.list()
            model_names = [model['name'] for model in models.get('models', [])]
            
            if self.model not in model_names:
                logger.info(f"Model {self.model} not found, pulling...")
                self.client.pull(self.model)
                logger.info(f"Model {self.model} pulled successfully")
            else:
                logger.info(f"Model {self.model} is available")
            
            return True
        except Exception as e:
            logger.error(f"Error ensuring model availability: {e}")
            return False
    
    def generate_response(
        self, 
        query: str, 
        context_documents: List[Dict[str, Any]],
        temperature: Optional[float] = None,
        max_tokens: Optional[int] = None
    ) -> str:
        """
        Generate a response using the LLM with RAG context.
        
        Args:
            query: User's query
            context_documents: List of relevant documents from RAG
            temperature: Optional temperature override
            max_tokens: Optional max tokens override
            
        Returns:
            Generated response text
        """
        # Build context from documents
        context_text = self._build_context(context_documents)
        
        # Build prompt with context and query
        prompt = self._build_prompt(query, context_text)
        
        # Set parameters
        temp = temperature if temperature is not None else settings.ollama_temperature
        max_tok = max_tokens if max_tokens is not None else settings.ollama_max_tokens
        
        try:
            logger.info(f"Generating response for query: {query[:50]}...")
            
            response = self.client.generate(
                model=self.model,
                prompt=prompt,
                options={
                    'temperature': temp,
                    'num_predict': max_tok,
                }
            )
            
            result = response.get('response', '').strip()
            logger.info(f"Generated response: {result[:50]}...")
            
            return result
        except Exception as e:
            logger.error(f"Error generating response: {e}")
            raise
    
    def _build_context(self, documents: List[Dict[str, Any]]) -> str:
        """
        Build context text from documents.
        
        Args:
            documents: List of document dictionaries
            
        Returns:
            Formatted context text
        """
        if not documents:
            return "No relevant documents found."
        
        context_parts = []
        for i, doc in enumerate(documents, 1):
            text = doc.get('text', '')
            metadata = doc.get('metadata', {})
            source = metadata.get('source', 'Unknown')
            
            context_parts.append(f"[Document {i} - Source: {source}]\n{text}")
        
        return "\n\n".join(context_parts)
    
    def _build_prompt(self, query: str, context: str) -> str:
        """
        Build the full prompt for the LLM.
        
        Args:
            query: User's query
            context: Context text from documents
            
        Returns:
            Formatted prompt
        """
        prompt = f"""You are a helpful AI assistant. Answer the user's question based on the provided context documents.

Context:
{context}

Question: {query}

Instructions:
- Answer based primarily on the provided context
- If the context doesn't contain enough information, acknowledge this
- Be concise and accurate
- Cite which document(s) you're using if relevant

Answer:"""
        
        return prompt
