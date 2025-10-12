# Contributing to Supabase Documentation Generator

Thank you for your interest in contributing! This document provides guidelines and instructions for contributing to this project.

## Getting Started

### Prerequisites

- Python 3.11 or higher
- Git
- Basic understanding of YAML and Python

### Development Setup

1. Fork and clone the repository:

```bash
git clone https://github.com/yourusername/supabase-docs-generator
cd supabase-docs-generator
```

2. Install development dependencies:

```bash
make dev-install
```

3. Verify installation:

```bash
supabase-docs-gen list-sdks
```

## Development Workflow

### Making Changes

1. Create a new branch:

```bash
git checkout -b feature/your-feature-name
```

2. Make your changes following the code style guidelines

3. Test your changes:

```bash
make test
make lint
```

4. Commit your changes:

```bash
git add .
git commit -m "Description of your changes"
```

5. Push to your fork:

```bash
git push origin feature/your-feature-name
```

6. Open a Pull Request

### Code Style

This project follows Python best practices:

- **Black** for code formatting (line length: 100)
- **Ruff** for linting
- **Type hints** for all function signatures
- **Docstrings** for all public methods

Format your code before committing:

```bash
make format
```

### Testing

Add tests for new functionality:

```python
# tests/test_parser.py
def test_parse_operation():
    # Your test here
    pass
```

Run tests:

```bash
make test
```

## Adding a New SDK

To add support for a new Supabase SDK:

1. Add SDK configuration to `config/sdks.yaml`:

```yaml
your_sdk:
  name: "YourSDK"
  display_name: "Supabase YourSDK Client"
  language: yourlang
  spec:
    url: "https://raw.githubusercontent.com/supabase/supabase/master/apps/docs/spec/supabase_yoursdk_v2.yml"
  output:
    base_dir: "yoursdk"
    filename_prefix: "supabase-yoursdk"
```

2. Verify operation IDs match categories in `config/categories.yaml`

3. Test generation:

```bash
supabase-docs-gen generate --sdk your_sdk --verbose
```

4. Review output for completeness

5. Submit PR with configuration and sample output

## Project Structure

```
src/supabase_docs_generator/
├── cli.py              # CLI interface (entry point)
├── core/
│   ├── models.py       # Data models
│   ├── parser.py       # YAML parser
│   └── formatter.py    # Documentation formatter
├── config/
│   ├── loader.py       # Config loader
│   └── schemas.py      # Pydantic schemas
└── utils/
    ├── logger.py       # Logging
    └── fetcher.py      # HTTP utilities
```

**Note**: The `scripts/` directory has been removed. All functionality is now provided through the CLI (`supabase-docs-gen`).

## Code Guidelines

### Python Style

- Use type hints for all parameters and return values
- Add docstrings to all public classes and methods
- Keep functions focused and single-purpose
- Use descriptive variable names
- Follow PEP 8 conventions

### Documentation

- Update README.md for user-facing changes
- Add docstrings for new functions
- Include examples in docstrings where helpful
- Update CHANGELOG.md

### Commit Messages

Use clear, descriptive commit messages:

```
feat: add support for JavaScript SDK
fix: resolve parsing error for nested examples
docs: update installation instructions
refactor: simplify category matching logic
test: add tests for formatter module
```

## Reporting Issues

When reporting issues, please include:

1. Python version
2. Operating system
3. Full error message and traceback
4. Steps to reproduce
5. Expected vs actual behavior

## Feature Requests

Feature requests are welcome! Please:

1. Check existing issues first
2. Describe the use case clearly
3. Explain expected behavior
4. Provide examples if applicable

## Questions?

Feel free to open an issue for questions or discussions.

## License

By contributing, you agree that your contributions will be licensed under the MIT License.
