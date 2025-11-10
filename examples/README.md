# Examples

This directory contains example scripts demonstrating how to use the RAG system API.

## test_api.py

A comprehensive example that demonstrates all API endpoints:

- Adding documents to the RAG system
- Querying for relevant documents
- Getting system statistics
- Deleting documents

### Usage

1. Make sure the RAG system is running:
   ```bash
   docker compose up -d
   ```

2. Run the example script:
   ```bash
   python examples/test_api.py
   ```

   Or directly:
   ```bash
   ./examples/test_api.py
   ```

### Expected Output

The script will:
1. Check the API health
2. Add 5 sample documents
3. Show system statistics
4. Run 4 different queries
5. Delete one document
6. Show final statistics

You should see detailed output for each operation, including response codes and JSON responses.
