"""Pytest configuration and fixtures."""

import pytest
import tempfile
import shutil
from pathlib import Path


@pytest.fixture(scope="function", autouse=True)
def temp_chroma_dir(monkeypatch):
    """Create a temporary ChromaDB directory for each test."""
    temp_dir = tempfile.mkdtemp()
    monkeypatch.setenv("CHROMA_PERSIST_DIRECTORY", temp_dir)
    yield temp_dir
    # Cleanup
    shutil.rmtree(temp_dir, ignore_errors=True)
