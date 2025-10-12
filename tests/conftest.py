"""Pytest configuration and fixtures."""

import pytest
from pathlib import Path


@pytest.fixture
def test_data_dir():
    """Return path to test data directory."""
    return Path(__file__).parent / "fixtures"


@pytest.fixture
def sample_spec_yaml():
    """Sample OpenRef YAML specification for testing."""
    return """
openref: 0.1

info:
  id: reference/test-sdk
  title: Test SDK
  description: Test SDK for unit tests

functions:
  - id: test-operation
    title: Test Operation
    description: A test operation
    examples:
      - id: test-example
        name: Test Example
        code: |
          ```swift
          let result = await test()
          ```
"""
