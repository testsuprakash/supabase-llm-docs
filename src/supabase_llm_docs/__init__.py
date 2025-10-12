"""Supabase Documentation Generator for LLMs.

Generate LLM-optimized documentation from official Supabase SDK specifications.
"""

__version__ = "1.0.0"
__author__ = "Supabase Docs Generator Contributors"

from .core.parser import OpenRefParser
from .core.formatter import LLMFormatter
from .core.models import Example, Operation, SpecData, SpecInfo

__all__ = [
    "OpenRefParser",
    "LLMFormatter",
    "Example",
    "Operation",
    "SpecData",
    "SpecInfo",
]
