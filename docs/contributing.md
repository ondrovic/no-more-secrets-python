# Contributing

Thank you for your interest in contributing to No More Secrets Python! This document provides guidelines for contributing to the project.

## Development Setup

### Prerequisites

- Python 3.10 or higher
- Poetry for dependency management
- Git for version control

### Getting Started

1. **Fork and clone the repository**:
   ```bash
   git clone https://github.com/ondrovic/no-more-secrets-python.git
   cd no-more-secrets-python
   ```

2. **Install dependencies**:
   ```bash
   poetry install --with dev
   ```

3. **Install pre-commit hooks**:
   ```bash
   poetry run pre-commit install
   ```

4. **Run tests to ensure everything works**:
   ```bash
   poetry run pytest
   ```

## Development Workflow

### Making Changes

1. **Create a feature branch**:
   ```bash
   git checkout -b feature/your-feature-name
   ```

2. **Make your changes** following our coding standards

3. **Run the test suite**:
   ```bash
   # Run all tests
   make test
   
   # Run specific tests
   poetry run pytest tests/test_your_module.py
   
   # Run with coverage
   poetry run pytest --cov=no_more_secrets
   ```

4. **Run code quality checks**:
   ```bash
   # Format code
   make format
   
   # Run linting
   make lint
   
   # Or run all checks
   poetry run pre-commit run --all-files
   ```

5. **Commit your changes**:
   ```bash
   git add .
   git commit -m "feat: add your feature description"
   ```

6. **Push and create a pull request**:
   ```bash
   git push origin feature/your-feature-name
   ```

## Coding Standards

### Code Style

- **Black** for code formatting (line length: 88)
- **isort** for import sorting
- **flake8** for linting
- **mypy** for type checking

### Code Quality

- Write comprehensive tests for new features
- Maintain test coverage above 90%
- Add type hints to all functions and methods
- Write clear, descriptive docstrings
- Follow Python naming conventions

### Commit Messages

Use conventional commit format:
- `feat:` for new features
- `fix:` for bug fixes
- `docs:` for documentation changes
- `test:` for test-related changes
- `refactor:` for code refactoring
- `style:` for formatting changes

## Testing

### Writing Tests

- Place tests in the `tests/` directory
- Name test files `test_*.py`
- Use descriptive test function names
- Test both happy path and edge cases
- Mock external dependencies when appropriate

### Test Categories

- **Unit tests**: Test individual functions and methods
- **Integration tests**: Test component interactions
- **Platform tests**: Test cross-platform compatibility
- **CLI tests**: Test command-line interfaces

### Running Tests

```bash
# All tests
poetry run pytest

# With coverage
poetry run pytest --cov=no_more_secrets --cov-report=html

# Specific test file
poetry run pytest tests/test_nms_effect.py

# Tests matching pattern
poetry run pytest -k "test_colors"

# Verbose output
poetry run pytest -v
```

## Documentation

### Docstrings

Use Google-style docstrings:

```python
def example_function(param1: str, param2: int = 0) -> bool:
    """Brief description of the function.

    Args:
        param1: Description of param1.
        param2: Description of param2. Defaults to 0.

    Returns:
        Description of return value.

    Raises:
        ValueError: Description of when this is raised.
    """
    pass
```

### Documentation Site

- Documentation is built with MkDocs Material
- Main content should be in the README.md
- API documentation is auto-generated from docstrings
- Build docs locally: `poetry run mkdocs serve`

## Pull Request Process

### Before Submitting

- [ ] Tests pass locally
- [ ] Code is formatted and linted
- [ ] Documentation is updated
- [ ] Commit messages follow conventions
- [ ] Branch is up to date with main

### PR Description

Include in your PR description:
- Summary of changes
- Type of change (feature, bugfix, etc.)
- Testing performed
- Screenshots/demos if applicable
- Breaking changes (if any)

### Review Process

1. Automated CI checks must pass
2. Code review by maintainers
3. Address any feedback
4. Approval and merge

## Issue Reporting

### Bug Reports

Include:
- Python version
- Operating system
- Steps to reproduce
- Expected vs actual behavior
- Error messages/stack traces
- Minimal code example

### Feature Requests

Include:
- Use case description
- Proposed solution
- Alternative solutions considered
- Implementation willingness

## Release Process

Releases are handled by maintainers:

1. Update version in `pyproject.toml`
2. Update `CHANGELOG.md`
3. Create release PR
4. Tag release after merge
5. GitHub Actions publishes to PyPI

## Getting Help

- **Questions**: Open a Discussion on GitHub
- **Bugs**: Open an Issue with the bug template
- **Features**: Open an Issue with the feature template
- **Chat**: Join our community discussions

## Code of Conduct

- Be respectful and inclusive
- Provide constructive feedback
- Help others learn and grow
- Focus on what's best for the community

## Recognition

Contributors are recognized in:
- README.md contributors section
- Release notes
- Documentation credits

Thank you for contributing to No More Secrets Python! 🎉