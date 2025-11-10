"""Configuration for the RAG system."""

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Application settings."""
    
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")
    
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
    
    # Ollama settings for LLM integration
    ollama_host: str = "http://localhost:11434"
    ollama_model: str = "qwen2.5:0.5b"
    ollama_temperature: float = 0.7
    ollama_max_tokens: int = 512


settings = Settings()
