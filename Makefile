.PHONY: help install dev up down logs restart clean test example

help: ## Show this help message
	@echo "Available commands:"
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "  \033[36m%-15s\033[0m %s\n", $$1, $$2}'

install: ## Install dependencies using UV
	uv pip install -e .

dev: ## Install development dependencies
	uv pip install -e ".[dev]"

up: ## Start the RAG system with Docker Compose
	docker compose up -d

down: ## Stop the RAG system
	docker compose down

logs: ## View logs from the RAG system
	docker compose logs -f

restart: ## Restart the RAG system
	docker compose restart

clean: ## Stop and remove all containers, volumes, and data
	docker compose down -v
	rm -rf data/

test: ## Run tests
	pytest tests/ -v

example: ## Run the example API test script
	python examples/test_api.py

build: ## Build Docker image
	docker compose build

shell: ## Open a shell in the running container
	docker compose exec rag-app /bin/bash

stats: ## Show system statistics
	curl http://localhost:8000/stats | jq

health: ## Check API health
	curl http://localhost:8000/health | jq
