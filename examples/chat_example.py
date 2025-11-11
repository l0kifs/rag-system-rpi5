#!/usr/bin/env python3
"""
Example script demonstrating the chat functionality with LLM integration.

This script shows how to:
1. Add documents to the RAG system
2. Query the RAG system for relevant documents
3. Use the chat endpoint to get LLM-powered responses
"""

import requests
import json
import time
from typing import Dict, Any


# Configuration
BASE_URL = "http://localhost:8000"


def add_document(text: str, metadata: Dict[str, Any] = None) -> Dict:
    """Add a document to the RAG system."""
    response = requests.post(
        f"{BASE_URL}/documents",
        json={"text": text, "metadata": metadata or {}}
    )
    response.raise_for_status()
    return response.json()


def query_documents(query: str, top_k: int = 5) -> Dict:
    """Query the RAG system for relevant documents."""
    response = requests.post(
        f"{BASE_URL}/query",
        json={"query": query, "top_k": top_k}
    )
    response.raise_for_status()
    return response.json()


def chat(query: str, top_k: int = 3, temperature: float = 0.7, max_tokens: int = 512) -> Dict:
    """Chat with the LLM using RAG context."""
    response = requests.post(
        f"{BASE_URL}/chat",
        json={
            "query": query,
            "top_k": top_k,
            "temperature": temperature,
            "max_tokens": max_tokens
        }
    )
    response.raise_for_status()
    return response.json()


def print_chat_response(response: Dict):
    """Pretty print a chat response."""
    print("\n" + "="*80)
    print(f"Question: {response['query']}")
    print("-"*80)
    print(f"Answer ({response['model']}):")
    print(response['response'])
    print("-"*80)
    print(f"Based on {len(response['sources'])} source document(s):")
    for i, source in enumerate(response['sources'], 1):
        metadata = source.get('metadata', {})
        print(f"  {i}. {metadata.get('source', 'Unknown')} (relevance: {1 - source['distance']:.2f})")
    print("="*80 + "\n")


def main():
    """Run the example."""
    print("RAG System with LLM - Chat Example")
    print("="*80)
    
    # Check if the API is available
    try:
        response = requests.get(f"{BASE_URL}/health")
        response.raise_for_status()
        print("✓ API is available")
    except Exception as e:
        print(f"✗ Cannot connect to API: {e}")
        print("\nPlease ensure the RAG system is running:")
        print("  docker-compose up -d")
        return
    
    # Add sample documents
    print("\n1. Adding sample documents...")
    documents = [
        {
            "text": "Machine learning is a subset of artificial intelligence that focuses on building systems that can learn from and make decisions based on data. It uses algorithms to identify patterns in data and improve performance over time without being explicitly programmed.",
            "metadata": {"source": "ml_intro.txt", "topic": "machine learning"}
        },
        {
            "text": "Deep learning is a subset of machine learning that uses neural networks with multiple layers. These deep neural networks can automatically learn hierarchical representations of data, making them particularly effective for tasks like image recognition and natural language processing.",
            "metadata": {"source": "deep_learning.txt", "topic": "deep learning"}
        },
        {
            "text": "Python is a high-level, interpreted programming language known for its simplicity and readability. It has become the most popular language for machine learning and data science due to its extensive libraries like NumPy, pandas, scikit-learn, and TensorFlow.",
            "metadata": {"source": "python_ml.txt", "topic": "python"}
        },
        {
            "text": "Neural networks are computing systems inspired by biological neural networks. They consist of interconnected nodes (neurons) organized in layers that can learn to perform tasks by processing examples and adjusting connection weights.",
            "metadata": {"source": "neural_nets.txt", "topic": "neural networks"}
        }
    ]
    
    for doc in documents:
        result = add_document(doc["text"], doc["metadata"])
        print(f"  ✓ Added: {doc['metadata']['source']} (ID: {result['id']})")
    
    # Wait a moment for indexing
    time.sleep(1)
    
    # Example 1: Simple question
    print("\n2. Example 1: Simple Question")
    print("-"*80)
    try:
        result = chat(
            query="What is machine learning?",
            top_k=2
        )
        print_chat_response(result)
    except requests.exceptions.HTTPError as e:
        if e.response.status_code == 503:
            print("✗ LLM service is not available. Please ensure:")
            print("  1. Ollama container is running: docker ps | grep ollama")
            print("  2. Model is installed: docker exec ollama ollama list")
            print("  3. Install model: ./scripts/install_model.sh")
        else:
            print(f"✗ Error: {e}")
        return
    
    # Example 2: Comparative question
    print("\n3. Example 2: Comparative Question")
    print("-"*80)
    result = chat(
        query="What's the difference between machine learning and deep learning?",
        top_k=3,
        temperature=0.7
    )
    print_chat_response(result)
    
    # Example 3: Specific question
    print("\n4. Example 3: Specific Question")
    print("-"*80)
    result = chat(
        query="Why is Python popular for machine learning?",
        top_k=2,
        temperature=0.5
    )
    print_chat_response(result)
    
    # Example 4: Compare with traditional RAG query
    print("\n5. Comparison: Traditional RAG Query vs. LLM-Powered Chat")
    print("-"*80)
    
    query = "Explain neural networks"
    
    print(f"\nTraditional Query (no LLM):")
    print("-"*40)
    query_result = query_documents(query, top_k=2)
    for i, doc in enumerate(query_result['results'], 1):
        print(f"{i}. {doc['text'][:100]}...")
        print(f"   Source: {doc['metadata'].get('source', 'Unknown')}\n")
    
    print("\nLLM-Powered Chat:")
    print("-"*40)
    chat_result = chat(query, top_k=2, temperature=0.6)
    print(chat_result['response'])
    
    print("\n" + "="*80)
    print("Example complete!")
    print("\nTry the interactive mode:")
    print("  python examples/test_api.py")
    print("\nOr use curl:")
    print(f"  curl -X POST {BASE_URL}/chat \\")
    print("    -H 'Content-Type: application/json' \\")
    print("    -d '{\"query\": \"Your question here\", \"top_k\": 3}'")


if __name__ == "__main__":
    main()
