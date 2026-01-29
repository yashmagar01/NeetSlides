# Contributing to NeetSlides

Thank you for your interest in contributing to NeetSlides! This document
provides guidelines for contributing.

## Development Setup

```bash
# Clone the repository
git clone https://github.com/YOUR_USERNAME/neetslides.git
cd neetslides

# Create a virtual environment
python -m venv .venv
.venv\Scripts\activate  # Windows
# source .venv/bin/activate  # Linux/Mac

# Install in development mode with dev dependencies
pip install -e ".[dev]"
```

## Code Style

We use [Ruff](https://github.com/astral-sh/ruff) for linting and formatting:

```bash
# Check for issues
ruff check src/

# Auto-fix issues
ruff check --fix src/

# Format code
ruff format src/
```

## Type Checking

We use [mypy](https://mypy.readthedocs.io/) for type checking:

```bash
mypy src/neetslides/
```

## Testing

We use [pytest](https://pytest.org/) for testing:

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=src/neetslides --cov-report=html
```

## Pull Request Process

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Make your changes
4. Run linting and tests
5. Commit your changes (`git commit -m 'Add amazing feature'`)
6. Push to the branch (`git push origin feature/amazing-feature`)
7. Open a Pull Request

## Commit Messages

Use clear, descriptive commit messages:

- `feat:` for new features
- `fix:` for bug fixes
- `docs:` for documentation changes
- `refactor:` for code refactoring
- `test:` for adding tests

## License

By contributing, you agree that your contributions will be licensed under the
Apache 2.0 License.
