# Architecture Documentation

## Overview

The Supabase Documentation Generator is a Python-based tool that transforms official OpenRef YAML specifications into LLM-optimized documentation.

## Design Principles

1. **Configuration-Driven**: All SDK and category definitions are externalized in YAML
2. **Type-Safe**: Pydantic schemas validate configurations
3. **Separation of Concerns**: Clear separation between parsing, formatting, and CLI
4. **Extensible**: Easy to add new SDKs without code changes
5. **Production-Ready**: Proper logging, error handling, and testing infrastructure

## Architecture Layers

### 1. CLI Layer (`cli.py`)

**Responsibility**: User interaction and command orchestration

- Click-based command-line interface
- Three main commands: `generate`, `validate`, `list-sdks`
- Rich terminal output for better UX
- Error handling and user feedback

### 2. Configuration Layer (`config/`)

**Responsibility**: Load and validate configuration

**Components**:
- `loader.py`: ConfigLoader class for reading YAML files
- `schemas.py`: Pydantic models for type-safe configuration
- `sdks.yaml`: SDK definitions (sources, output settings)
- `categories.yaml`: Module categorization and operation groupings

**Key Features**:
- Automatic validation via Pydantic
- Support for local and remote spec sources
- Ordered category processing
- SDK-specific metadata

### 3. Core Layer (`core/`)

**Responsibility**: Parsing and formatting logic

**Components**:

#### `models.py` - Data Models
- `Example`: Code example with SQL/JSON context
- `Operation`: API operation with examples and metadata
- `SpecInfo`: Specification metadata
- `SpecData`: Complete parsed specification

#### `parser.py` - OpenRef Parser
- Parses OpenRef 0.1 YAML format
- Extracts operations, examples, and metadata
- Saves intermediate JSON for debugging
- Proper logging and error handling

#### `formatter.py` - LLM Formatter
- Generates token-optimized documentation
- Inline SQL schemas and JSON responses
- Hierarchical numbering for navigation
- Supports modular and full documentation

### 4. Utilities Layer (`utils/`)

**Responsibility**: Cross-cutting concerns

**Components**:
- `logger.py`: Structured logging setup
- `fetcher.py`: HTTP spec downloading from GitHub

## Data Flow

```
1. User runs CLI command
   ↓
2. ConfigLoader reads YAML configs
   ↓
3. Fetcher downloads spec from GitHub
   ↓
4. Parser extracts structured data
   ↓
5. Parser saves intermediate JSON
   ↓
6. Formatter categorizes operations
   ↓
7. Formatter generates module docs
   ↓
8. Formatter combines into full doc
   ↓
9. Files written to output directory
```

## File Organization

```
supabase-docs-generator/
├── src/supabase_docs_generator/    # Source code
│   ├── __init__.py
│   ├── __main__.py
│   ├── cli.py                       # CLI entry point
│   ├── core/                        # Core logic
│   │   ├── models.py                # Data models
│   │   ├── parser.py                # YAML parser
│   │   └── formatter.py             # Doc formatter
│   ├── config/                      # Configuration
│   │   ├── loader.py                # Config loader
│   │   └── schemas.py               # Pydantic schemas
│   └── utils/                       # Utilities
│       ├── logger.py                # Logging
│       └── fetcher.py               # HTTP fetcher
├── config/                          # Configuration files
│   ├── sdks.yaml                    # SDK definitions
│   └── categories.yaml              # Categorization
├── output/                          # Generated docs
│   └── {sdk}/
│       ├── parsed/                  # Intermediate JSON
│       └── llm-docs/                # Final documentation
├── tests/                           # Test suite
├── docs/                            # Documentation
├── pyproject.toml                   # Project config
├── Makefile                         # Dev commands
└── README.md                        # User docs
```

## OpenRef Format

The tool parses OpenRef 0.1, Supabase's specification format:

```yaml
openref: 0.1

info:
  id: reference/sdk-name
  title: SDK Title
  description: SDK description

functions:
  - id: operation-id
    title: Operation Title
    description: Operation description
    notes: Important notes
    examples:
      - id: example-id
        name: Example Name
        code: |
          code here
        data:
          sql: |
            setup SQL
        response: |
          expected output
```

## Output Format

Generated documentation optimized for LLM consumption:

```
<SYSTEM>System prompt for context</SYSTEM>

# SDK Title - Module Documentation

Module description

# 1. Operation Title

Operation description and notes

## 1.1. Example Name

```language
code here

// Data Source
/*
setup SQL
*/

// Response
/*
expected output
*/
```

// Note: Additional context
```

## Extension Points

### Adding a New SDK

1. Add entry to `config/sdks.yaml`
2. Verify operations match `config/categories.yaml`
3. Run generation

### Adding a New Category

1. Add entry to `config/categories.yaml`
2. Specify operations that belong to category
3. Set order for documentation

### Custom Formatting

Extend `LLMFormatter` class to implement custom output formats:

```python
class CustomFormatter(LLMFormatter):
    def _format_example(self, example, section_num, example_num):
        # Custom formatting logic
        pass
```

## Performance Considerations

- **Streaming**: Not yet implemented; all data loaded into memory
- **Caching**: Fetcher caches specs in config directory
- **Parallelization**: Single-threaded; could parallelize multiple SDKs

## Security Considerations

- **Input Validation**: Pydantic validates all configuration
- **Path Traversal**: All paths resolved and validated
- **HTTP Requests**: Timeout and error handling on fetches
- **No Eval**: No dynamic code execution

## Testing Strategy

- **Unit Tests**: Core parsing and formatting logic
- **Integration Tests**: End-to-end generation
- **Fixtures**: Sample specs for testing
- **Validation**: Schema validation via Pydantic

## Future Enhancements

1. Support for additional spec formats (OpenAPI, AsyncAPI)
2. Incremental generation (only changed operations)
3. Multiple output formats (JSON, JSONL)
4. Web UI for configuration
5. Plugin system for custom formatters
6. Parallel SDK processing
7. Streaming for large specs
8. Documentation diffing
9. RAG embeddings generation
10. Integration with CI/CD
