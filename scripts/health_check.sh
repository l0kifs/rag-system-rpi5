#!/bin/bash
# Simple health check script for the RAG system

set -e

URL="${RAG_API_URL:-http://localhost:8000}"

echo "Checking RAG System health at $URL..."

# Check if the API is responding
if curl -f -s "$URL/health" > /dev/null; then
    echo "✅ RAG System is healthy!"
    curl -s "$URL/health" | jq . 2>/dev/null || curl -s "$URL/health"
    exit 0
else
    echo "❌ RAG System is not responding!"
    exit 1
fi
