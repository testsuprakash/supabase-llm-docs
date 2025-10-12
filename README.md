# Supabase LLM Documentation Generator

> Generate token-efficient, LLM-optimized documentation from official Supabase SDK specifications

[![Python](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

## What This Does

Transforms Supabase's official OpenRef YAML specifications into **token-efficient, context-rich documentation** specifically optimized for Large Language Models (Claude, GPT, etc.).

**Key Features:**
- Inline SQL schemas and JSON responses for better context
- Token-optimized format (minimal decorations, maximum information)
- Modular output (separate files for auth, database, storage, etc.)
- Automated fetching from Supabase's official specs
- **Complete support for all 6 Supabase SDKs across 11 versions**

## Supported SDKs

**Complete support for all 6 Supabase SDKs across 11 versions:**

- **JavaScript/TypeScript**: v1, v2 (2 versions)
- **Kotlin**: v1, v2, v3 (3 versions)
- **Dart/Flutter**: v1, v2 (2 versions)
- **C#**: v0, v1 (2 versions)
- **Python**: v2 (1 version)
- **Swift**: v1, v2 (2 versions)

Total: 11 specification files supported

## Quick Start

### Installation

```bash
git clone https://github.com/Zyepher/supabase-llm-docs
cd supabase-llm-docs
pip install -e .
```

### Generate Documentation

**List available SDKs:**
```bash
supabase-llm-docs list-sdks
```

**Generate specific SDK (latest version):**
```bash
supabase-llm-docs generate --sdk javascript
supabase-llm-docs generate --sdk swift
supabase-llm-docs generate --sdk kotlin
```

**Generate specific version:**
```bash
supabase-llm-docs generate --sdk javascript --version v2
supabase-llm-docs generate --sdk kotlin --version v3
```

**Generate all versions:**
```bash
supabase-llm-docs generate --sdk javascript --version all
```

**Generate everything:**
```bash
supabase-llm-docs generate --sdk all --version all
```

**Using Make (recommended):**
```bash
make list            # List all SDKs and versions
make run-js          # Generate JavaScript (latest)
make run-kotlin      # Generate Kotlin (latest)
make run-swift       # Generate Swift (latest)
make run             # Generate all SDKs (all versions)
```

### Output Location

Generated documentation is saved in:
```
output/
├── javascript/
│   ├── v2/
│   │   ├── parsed/
│   │   │   └── javascript-v2-spec.json
│   │   └── llm-docs/
│   │       ├── supabase-js-v2-initializing-llms.txt
│   │       ├── supabase-js-v2-database-llms.txt
│   │       ├── supabase-js-v2-auth-llms.txt
│   │       ├── supabase-js-v2-storage-llms.txt
│   │       ├── supabase-js-v2-realtime-llms.txt
│   │       ├── supabase-js-v2-edge-functions-llms.txt
│   │       └── supabase-js-v2-full-llms.txt
│   └── v1/
│       └── ...
├── kotlin/
│   ├── v3/
│   ├── v2/
│   └── v1/
├── swift/
├── dart/
├── csharp/
└── python/
```

## Using Generated Documentation

### With LLMs

Copy the generated `.txt` files into your LLM context:

**For complete reference:**
- Use `*-full-llms.txt` - includes all SDK functionality

**For specific topics:**
- Use individual module files (auth, database, storage, etc.)
- More token-efficient when you only need specific functionality

**Example with Claude:**
```
Paste supabase-js-v2-database-llms.txt into your conversation, then ask:
"How do I query a PostgreSQL table with filters in JavaScript?"
```

### Documentation Format

The generated docs use an LLM-optimized format:

```markdown
<SYSTEM>This is the developer documentation for Supabase JavaScript Client v2 - Database Operations.</SYSTEM>

# Supabase JavaScript Client v2 Database Operations Documentation

# 1. Fetch data: select()

## 1.1. Getting your data

```javascript
const { data, error } = await supabase
  .from('countries')
  .select()

// Data Source
/*
create table countries (
  id int8 primary key,
  name text
);
*/

// Response
/*
{
  "data": [{"id": 1, "name": "Afghanistan"}],
  "status": 200
}
*/
```
```

**Why this format?**
- System prompts provide context to LLMs
- SQL schemas embedded in code blocks
- Expected responses inline
- Hierarchical numbering for navigation
- Token-efficient (no decorative elements)

## Development

### Setup Development Environment

```bash
# Install with development dependencies
pip install -e ".[dev]"
```

### Available Commands

```bash
make install         # Install package
make dev-install     # Install with dev dependencies
make clean           # Remove generated files
make test            # Run tests
make lint            # Run linters
make format          # Format code
make list            # List all SDKs and versions
make run             # Generate docs for all SDKs
make run-js          # Generate JavaScript docs (latest)
make run-kotlin      # Generate Kotlin docs (latest)
make run-swift       # Generate Swift docs (latest)
```

### Run Tests

```bash
make test

# Or with pytest directly
pytest
```

### Code Quality

```bash
# Lint code
make lint

# Format code
make format
```

## Configuration

The tool uses configuration-driven design with zero code changes needed to add SDKs.

### SDK Configuration (`config/sdks.yaml`)

```yaml
sdks:
  javascript:
    name: "JavaScript"
    language: javascript
    versions:
      v2:
        display_name: "Supabase JavaScript Client v2"
        spec:
          url: "https://raw.githubusercontent.com/supabase/supabase/master/apps/docs/spec/supabase_js_v2.yml"
        output:
          base_dir: "javascript"
          filename_prefix: "supabase-js-v2"
      v1:
        display_name: "Supabase JavaScript Client v1"
        spec:
          url: "https://raw.githubusercontent.com/supabase/supabase/master/apps/docs/spec/supabase_js_v1.yml"
        output:
          base_dir: "javascript"
          filename_prefix: "supabase-js-v1"
```

### Category Configuration (`config/categories.yaml`)

Controls how operations are grouped into modules:

```yaml
categories:
  database:
    title: "Database Operations"
    description: "Query and manipulate data using PostgREST"
    operations:
      - select
      - insert
      - update
      - delete
      # ... more operations
    order: 4
```

## Project Structure

```
supabase-llm-docs/
├── src/supabase_llm_docs/    # Core Python package
│   ├── cli.py                 # Command-line interface
│   ├── core/
│   │   ├── parser.py          # OpenRef YAML parser
│   │   ├── formatter.py       # LLM documentation formatter
│   │   └── models.py          # Data models
│   ├── config/
│   │   ├── loader.py          # Configuration management
│   │   └── schemas.py         # Pydantic validation schemas
│   └── utils/
│       ├── logger.py          # Logging setup
│       └── fetcher.py         # HTTP spec fetching
├── config/
│   ├── sdks.yaml              # SDK definitions
│   └── categories.yaml        # Module categorization
├── output/                    # Generated documentation
├── tests/                     # Test suite
├── pyproject.toml             # Project configuration
├── Makefile                   # Development commands
└── README.md                  # This file
```

## Architecture

The tool follows a three-stage pipeline:

1. **Fetch**: Download latest YAML specs from GitHub (or use local files)
2. **Parse**: Extract operations, examples, and metadata into structured data
3. **Format**: Transform into LLM-optimized documentation with inline context

All configuration is data-driven via YAML files, making it easy to:
- Add new SDKs without code changes
- Modify operation categorization
- Customize output formats
- Extend functionality

## CLI Commands

### `generate`

Generate LLM documentation for specified SDK(s) and version(s).

```bash
supabase-llm-docs generate --sdk <sdk_name> [--version <version>]

Options:
  --sdk TEXT          SDK to generate (javascript, kotlin, swift, dart, csharp, python, or 'all')
  --version TEXT      Version to generate (v1, v2, v3, 'latest', or 'all') [default: latest]
  --config-dir PATH   Configuration directory [default: config]
  --output-dir PATH   Output directory [default: output]
  -v, --verbose       Enable verbose logging
```

### `list-sdks`

List all configured SDKs and their versions.

```bash
supabase-llm-docs list-sdks
```

### `validate`

Validate SDK specification.

```bash
supabase-llm-docs validate <sdk_name> [--version <version>]
```

## Contributing

Contributions are welcome! Please see [CONTRIBUTING.md](CONTRIBUTING.md) for:
- Development workflow
- Code style guidelines
- Testing requirements
- Pull request process

### Quick Contributing Guide

1. Fork the repository
2. Create a feature branch: `git checkout -b feature/your-feature`
3. Make your changes
4. Run tests: `make test`
5. Format code: `make format`
6. Commit: `git commit -m "feat: your feature"`
7. Push and create a Pull Request

## License

MIT License - see [LICENSE](LICENSE) for details.

## Acknowledgments

- Built for the [Supabase](https://supabase.com) ecosystem
- Uses Supabase's OpenRef 0.1 specification format
- Official specs: [supabase/supabase/apps/docs/spec](https://github.com/supabase/supabase/tree/master/apps/docs/spec)

## Links

- [Supabase](https://supabase.com)
- [Supabase GitHub](https://github.com/supabase/supabase)
- [OpenRef Specifications](https://github.com/supabase/supabase/tree/master/apps/docs/spec)

## Version History

See [CHANGELOG.md](CHANGELOG.md) for version history and release notes.
