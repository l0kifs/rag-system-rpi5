#!/bin/bash
# Script to install the default LLM model for the RAG system

set -e

# Colors for output
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

# Default model
MODEL="${1:-qwen2.5:0.5b}"

echo -e "${GREEN}Installing Ollama model: ${MODEL}${NC}"
echo ""

# Check if Ollama container is running
if ! docker ps | grep -q ollama; then
    echo -e "${YELLOW}Ollama container is not running.${NC}"
    echo "Starting services..."
    docker-compose up -d ollama
    
    echo "Waiting for Ollama to be ready..."
    sleep 10
fi

# Check if Ollama is accessible
if ! docker exec ollama ollama list > /dev/null 2>&1; then
    echo -e "${RED}Error: Cannot connect to Ollama${NC}"
    echo "Please ensure the Ollama container is running:"
    echo "  docker-compose up -d ollama"
    exit 1
fi

# List current models
echo -e "${GREEN}Current models:${NC}"
docker exec ollama ollama list

echo ""
echo -e "${GREEN}Pulling model: ${MODEL}${NC}"
echo "This may take a few minutes depending on your connection..."
echo ""

# Pull the model
if docker exec ollama ollama pull "${MODEL}"; then
    echo ""
    echo -e "${GREEN}✓ Model ${MODEL} installed successfully!${NC}"
    echo ""
    echo "You can now use the chat endpoint with this model."
    echo ""
    echo "To use a different model, update the OLLAMA_MODEL environment variable"
    echo "and restart the rag-app container:"
    echo ""
    echo "  export OLLAMA_MODEL=${MODEL}"
    echo "  docker-compose restart rag-app"
    echo ""
else
    echo ""
    echo -e "${RED}✗ Failed to install model ${MODEL}${NC}"
    echo "Please check your internet connection and try again."
    exit 1
fi

# List updated models
echo -e "${GREEN}Updated models:${NC}"
docker exec ollama ollama list
