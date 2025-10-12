"""Data models for OpenRef specification."""

from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional


@dataclass
class Example:
    """Code example from specification."""

    id: str
    name: str
    code: str
    description: str = ""
    data_sql: str = ""
    response: str = ""
    is_spotlight: bool = False

    def has_context(self) -> bool:
        """Check if example has SQL or response context."""
        return bool(self.data_sql or self.response)


@dataclass
class Operation:
    """API operation from specification."""

    id: str
    title: str
    description: str = ""
    notes: str = ""
    examples: List[Example] = field(default_factory=list)
    overwrite_params: List[Dict[str, Any]] = field(default_factory=list)

    @property
    def example_count(self) -> int:
        """Number of examples in this operation."""
        return len(self.examples)

    def get_spotlight_examples(self) -> List[Example]:
        """Get examples marked as spotlight."""
        return [ex for ex in self.examples if ex.is_spotlight]


@dataclass
class SpecInfo:
    """Specification metadata."""

    id: str
    title: str
    description: str
    spec_url: str = ""
    slug_prefix: str = "/"
    libraries: List[Dict[str, str]] = field(default_factory=list)


@dataclass
class SpecData:
    """Complete parsed specification."""

    info: SpecInfo
    operations: List[Operation]

    @property
    def total_examples(self) -> int:
        """Total number of examples across all operations."""
        return sum(op.example_count for op in self.operations)

    def get_operation_by_id(self, operation_id: str) -> Optional[Operation]:
        """Find operation by ID."""
        return next((op for op in self.operations if op.id == operation_id), None)

    def get_operations_by_ids(self, operation_ids: List[str]) -> List[Operation]:
        """Find multiple operations by their IDs."""
        id_set = set(operation_ids)
        return [op for op in self.operations if op.id in id_set]
