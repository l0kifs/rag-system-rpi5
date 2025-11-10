"""Configuration for the RAG system."""

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Application settings."""
    
    app_name: str = "RAG System RPi5"
    app_version: str = "0.1.0"
    
    # Embedding model optimized for ARM architecture
    embedding_model: str = "all-MiniLM-L6-v2"
    
    # ChromaDB settings
    chroma_persist_directory: str = "/data/chroma"
    collection_name: str = "rag_documents"
    
    # API settings
    max_upload_size: int = 10 * 1024 * 1024  # 10MB
    top_k_results: int = 5
    
    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


settings = Settings()
