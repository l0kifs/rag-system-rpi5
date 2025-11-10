# Use Python 3.11 slim image optimized for ARM64 (Raspberry Pi 5)
FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Install UV package manager
RUN curl -LsSf https://astral.sh/uv/install.sh | sh
ENV PATH="/root/.cargo/bin:$PATH"

# Copy project files
COPY pyproject.toml ./
COPY src ./src

# Install dependencies using UV
RUN uv pip install --system -e .

# Create data directory for ChromaDB persistence
RUN mkdir -p /data/chroma

# Expose port
EXPOSE 8000

# Run the application
CMD ["uvicorn", "rag_system_rpi5.main:app", "--host", "0.0.0.0", "--port", "8000"]
