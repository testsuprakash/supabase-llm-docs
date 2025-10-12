"""Tests for OpenRef parser."""

import pytest
from pathlib import Path
from supabase_llm_docs.core.parser import OpenRefParser
from supabase_llm_docs.core.models import SpecData


def test_parser_initialization():
    """Test parser can be initialized with a path."""
    parser = OpenRefParser(Path("test.yml"))
    assert parser.spec_path == Path("test.yml")


def test_parser_file_not_found():
    """Test parser raises error for non-existent file."""
    parser = OpenRefParser(Path("nonexistent.yml"))
    with pytest.raises(FileNotFoundError):
        parser.parse()


# Add more tests as needed
