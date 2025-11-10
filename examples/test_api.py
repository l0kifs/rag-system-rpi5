#!/usr/bin/env python3
"""
Example script to test the RAG system API.

This script demonstrates how to:
1. Add documents to the RAG system
2. Query the system for relevant documents
3. Get system statistics
4. Delete documents

Usage:
    python examples/test_api.py
"""

import requests
import json
import time

# API base URL
BASE_URL = "http://localhost:8000"


def print_response(title, response):
    """Pretty print API response."""
    print(f"\n{'='*60}")
    print(f"{title}")
    print(f"{'='*60}")
    print(f"Status Code: {response.status_code}")
    print(f"Response:")
    print(json.dumps(response.json(), indent=2))


def main():
    """Run the API test examples."""
    print("RAG System API Test")
    print("=" * 60)
    
    # 1. Check health
    print("\n1. Checking API health...")
    response = requests.get(f"{BASE_URL}/health")
    print_response("Health Check", response)
    
    # 2. Add sample documents
    print("\n2. Adding sample documents...")
    
    documents = [
        {
            "text": "Machine learning is a subset of artificial intelligence that focuses on building systems that learn from data.",
            "metadata": {"topic": "AI", "category": "definition", "source": "knowledge_base"}
        },
        {
            "text": "Python is a high-level, interpreted programming language known for its simplicity and readability.",
            "metadata": {"topic": "Programming", "category": "definition", "source": "knowledge_base"}
        },
        {
            "text": "The Raspberry Pi 5 is the latest single-board computer from the Raspberry Pi Foundation, featuring improved performance and new features.",
            "metadata": {"topic": "Hardware", "category": "product", "source": "knowledge_base"}
        },
        {
            "text": "Docker is a platform that enables developers to package applications into containers, which are lightweight, portable, and self-sufficient units.",
            "metadata": {"topic": "DevOps", "category": "tool", "source": "knowledge_base"}
        },
        {
            "text": "FastAPI is a modern, fast web framework for building APIs with Python 3.7+ based on standard Python type hints.",
            "metadata": {"topic": "Programming", "category": "framework", "source": "knowledge_base"}
        }
    ]
    
    doc_ids = []
    for i, doc in enumerate(documents, 1):
        response = requests.post(f"{BASE_URL}/documents", json=doc)
        print(f"  Added document {i}: {response.json()['id']}")
        doc_ids.append(response.json()['id'])
    
    # Give the system a moment to process
    time.sleep(1)
    
    # 3. Get system statistics
    print("\n3. Getting system statistics...")
    response = requests.get(f"{BASE_URL}/stats")
    print_response("System Statistics", response)
    
    # 4. Query documents
    print("\n4. Querying documents...")
    
    queries = [
        {"query": "What is machine learning?", "top_k": 3},
        {"query": "Tell me about Python programming language", "top_k": 2},
        {"query": "What are the features of Raspberry Pi?", "top_k": 2},
        {"query": "Explain containerization", "top_k": 2},
    ]
    
    for query in queries:
        response = requests.post(f"{BASE_URL}/query", json=query)
        print_response(f"Query: '{query['query']}'", response)
        
        # Print simplified results
        data = response.json()
        if data["count"] > 0:
            print("\nTop Results:")
            for i, result in enumerate(data["results"][:2], 1):
                print(f"  {i}. {result['text'][:100]}...")
                print(f"     Distance: {result['distance']:.4f}")
    
    # 5. Delete a document
    print("\n5. Deleting a document...")
    if doc_ids:
        response = requests.delete(f"{BASE_URL}/documents/{doc_ids[0]}")
        print_response(f"Delete document {doc_ids[0]}", response)
    
    # 6. Final statistics
    print("\n6. Final system statistics...")
    response = requests.get(f"{BASE_URL}/stats")
    print_response("Final Statistics", response)
    
    print("\n" + "="*60)
    print("API test completed successfully!")
    print("="*60)


if __name__ == "__main__":
    try:
        main()
    except requests.exceptions.ConnectionError:
        print("\n❌ Error: Could not connect to the API.")
        print("Make sure the RAG system is running:")
        print("  docker compose up -d")
        print("\nOr run locally:")
        print("  uvicorn rag_system_rpi5.main:app")
    except Exception as e:
        print(f"\n❌ Error: {e}")
