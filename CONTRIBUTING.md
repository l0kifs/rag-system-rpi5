# Contributing to RAG System for Raspberry Pi 5

Thank you for your interest in contributing to this project! This document provides guidelines and best practices for contributing.

## Development Setup

1. **Clone the repository:**
   ```bash
   git clone https://github.com/l0kifs/rag-system-rpi5.git
   cd rag-system-rpi5
   ```

2. **Install UV package manager:**
   ```bash
   curl -LsSf https://astral.sh/uv/install.sh | sh
   ```

3. **Install dependencies:**
   ```bash
   uv pip install -e ".[dev]"
   ```

## Code Style

This project follows Python best practices:

- **PEP 8** style guide
- **Type hints** for function parameters and return values
- **Docstrings** for all public functions and classes
- **Ruff** for linting and formatting

### Running Linter

```bash
ruff check src/ tests/
```

### Auto-fixing Issues

```bash
ruff check --fix src/ tests/
```

## Testing

Always add tests for new features:

1. **Write tests in `tests/` directory**
2. **Run tests locally:**
   ```bash
   pytest tests/ -v
   ```

3. **Ensure all tests pass before submitting PR**

## Making Changes

1. **Create a new branch:**
   ```bash
   git checkout -b feature/your-feature-name
   ```

2. **Make your changes**

3. **Test your changes:**
   ```bash
   # Run tests
   pytest tests/ -v
   
   # Test with Docker
   docker compose up --build
   python examples/test_api.py
   ```

4. **Commit with clear messages:**
   ```bash
   git commit -m "Add feature: description"
   ```

5. **Push and create a Pull Request**

## Pull Request Guidelines

- **Clear title and description**
- **Reference related issues**
- **Include tests for new features**
- **Update documentation if needed**
- **Ensure CI/CD passes**

## Best Practices

### For Raspberry Pi Optimization

1. **Use lightweight models** - The default `all-MiniLM-L6-v2` is optimized for ARM
2. **Consider memory constraints** - Raspberry Pi 5 has limited RAM
3. **Test on actual hardware** - Performance may differ from x86_64

### For Docker

1. **Keep images small** - Use slim base images
2. **Multi-stage builds** - If adding build dependencies
3. **Volume management** - Ensure data persistence

### For API Design

1. **RESTful principles** - Follow standard HTTP methods
2. **Clear error messages** - Help users debug issues
3. **Input validation** - Use Pydantic models
4. **API documentation** - Update OpenAPI/Swagger docs

## Documentation

Update documentation when:

- Adding new features
- Changing API endpoints
- Modifying configuration options
- Adding new dependencies

## Security

- **Never commit secrets** - Use environment variables
- **Validate all inputs** - Prevent injection attacks
- **Keep dependencies updated** - Run `uv pip list --outdated`

## Getting Help

- **Open an issue** for bugs or feature requests
- **Start a discussion** for questions or ideas
- **Check existing issues** before creating new ones

## License

By contributing, you agree that your contributions will be licensed under the MIT License.
