"""OpenRef YAML specification parser."""

import json
import logging
import yaml
from dataclasses import asdict
from pathlib import Path
from typing import Any, Dict, List

from .models import Example, Operation, SpecData, SpecInfo

logger = logging.getLogger(__name__)


class OpenRefParser:
    """Parse Supabase OpenRef YAML specifications."""

    def __init__(self, spec_path: Path):
        """Initialize parser with specification file path.

        Args:
            spec_path: Path to OpenRef YAML specification file
        """
        self.spec_path = Path(spec_path)

    def parse(self) -> SpecData:
        """Parse the YAML spec file and return structured data.

        Returns:
            SpecData object containing all parsed information

        Raises:
            FileNotFoundError: If spec file doesn't exist
            yaml.YAMLError: If YAML is malformed
        """
        if not self.spec_path.exists():
            raise FileNotFoundError(f"Spec file not found: {self.spec_path}")

        logger.info(f"Parsing specification: {self.spec_path}")

        with open(self.spec_path, "r", encoding="utf-8") as f:
            spec = yaml.safe_load(f)

        # Extract and parse info
        info_dict = spec.get("info", {})
        info = SpecInfo(
            id=info_dict.get("id", ""),
            title=info_dict.get("title", ""),
            description=info_dict.get("description", "").strip(),
            spec_url=info_dict.get("specUrl", ""),
            slug_prefix=info_dict.get("slugPrefix", "/"),
            libraries=info_dict.get("libraries", []),
        )

        # Extract operations (called 'functions' in OpenRef spec)
        operations = []
        functions = spec.get("functions", [])

        for func in functions:
            operation = self._parse_operation(func)
            operations.append(operation)
            logger.debug(
                f"Parsed operation: {operation.id} ({len(operation.examples)} examples)"
            )

        logger.info(
            f"Parsing complete: {len(operations)} operations, "
            f"{sum(len(op.examples) for op in operations)} total examples"
        )

        return SpecData(info=info, operations=operations)

    def _parse_operation(self, func: Dict[str, Any]) -> Operation:
        """Parse a single operation from the spec.

        Args:
            func: Operation dictionary from YAML

        Returns:
            Operation object
        """
        operation_id = func.get("id", "")
        title = func.get("title", "")
        description = func.get("description", "").strip()
        notes = func.get("notes", "").strip()
        overwrite_params = func.get("overwriteParams", [])

        # Parse examples
        examples = []
        for ex in func.get("examples", []):
            example = self._parse_example(ex)
            examples.append(example)

        return Operation(
            id=operation_id,
            title=title,
            description=description,
            notes=notes,
            examples=examples,
            overwrite_params=overwrite_params,
        )

    def _parse_example(self, ex: Dict[str, Any]) -> Example:
        """Parse a single example from the spec.

        Args:
            ex: Example dictionary from YAML

        Returns:
            Example object
        """
        example_id = ex.get("id", "")
        name = ex.get("name", "")
        code = ex.get("code", "").strip()
        description = ex.get("description", "").strip()
        is_spotlight = ex.get("isSpotlight", False)

        # Extract data source (SQL schema)
        data_sql = ""
        data_block = ex.get("data", {})
        if isinstance(data_block, dict):
            data_sql = data_block.get("sql", "").strip()

        # Extract response
        response = ex.get("response", "").strip()

        return Example(
            id=example_id,
            name=name,
            code=code,
            description=description,
            data_sql=data_sql,
            response=response,
            is_spotlight=is_spotlight,
        )

    def save_json(self, spec_data: SpecData, output_path: Path) -> None:
        """Save parsed data as JSON for the formatter.

        Args:
            spec_data: Parsed specification data
            output_path: Path to output JSON file
        """
        data = {
            "info": asdict(spec_data.info),
            "operations": [
                {
                    "id": op.id,
                    "title": op.title,
                    "description": op.description,
                    "notes": op.notes,
                    "examples": [asdict(ex) for ex in op.examples],
                    "overwrite_params": op.overwrite_params,
                }
                for op in spec_data.operations
            ],
        }

        output_path.parent.mkdir(parents=True, exist_ok=True)
        with open(output_path, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2, ensure_ascii=False)

        logger.info(f"Saved parsed data to {output_path}")
