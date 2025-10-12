"""LLM-optimized documentation formatter."""

import logging
from pathlib import Path
from typing import Dict, List

from .models import Example, Operation, SpecData
from ..config.loader import ConfigLoader
from ..config.schemas import SDKVersionConfig

logger = logging.getLogger(__name__)


class LLMFormatter:
    """Format parsed spec data into LLM-optimized documentation."""

    def __init__(
        self,
        spec_data: SpecData,
        config: ConfigLoader,
        sdk_name: str,
        version: str
    ):
        """Initialize formatter.

        Args:
            spec_data: Parsed specification data
            config: Configuration loader
            sdk_name: SDK name (e.g., 'swift', 'dart', 'javascript')
            version: Version string (e.g., 'v2', 'v1')
        """
        self.spec_data = spec_data
        self.config = config
        self.sdk_name = sdk_name
        self.version = version
        self.version_config = config.get_sdk_version(sdk_name, version)

    def generate_all(self, output_dir: Path) -> None:
        """Generate all documentation files.

        Args:
            output_dir: Base output directory for this SDK
        """
        output_dir = Path(output_dir)
        llm_docs_dir = output_dir / "llm-docs"
        llm_docs_dir.mkdir(parents=True, exist_ok=True)

        logger.info(f"Generating documentation for {self.sdk_name}")

        # Categorize operations
        categorized = self._categorize_operations()

        # Store module contents for full doc generation
        module_contents = {}

        # Generate documentation for each category
        for category_name, category_config in self.config.get_sorted_categories():
            if category_name in categorized and categorized[category_name]:
                logger.info(f"Formatting {category_name} module...")
                doc_content = self._format_module(category_name, categorized[category_name])
                self._write_module_file(llm_docs_dir, category_name, doc_content)
                module_contents[category_name] = doc_content

        # Generate full documentation
        logger.info("Generating full documentation...")
        self._generate_full_doc(llm_docs_dir, module_contents)

        logger.info(f"Documentation generation complete for {self.sdk_name}")

    def _categorize_operations(self) -> Dict[str, List[Operation]]:
        """Categorize operations by module.

        Returns:
            Dictionary mapping category names to lists of operations
        """
        categorized = {}
        uncategorized = []

        # Build operation ID to operation mapping
        operation_map = {op.id: op for op in self.spec_data.operations}

        # Categorize based on config
        for category_name, category_config in self.config.get_categories().items():
            category_ops = []
            for op_id in category_config.operations:
                if op_id in operation_map:
                    category_ops.append(operation_map[op_id])
                    # Mark as categorized
                    operation_map[op_id] = None

            categorized[category_name] = category_ops

        # Find uncategorized operations
        uncategorized = [op for op in operation_map.values() if op is not None]

        if uncategorized:
            logger.warning(
                f"{len(uncategorized)} operations not categorized: "
                f"{', '.join(op.id for op in uncategorized)}"
            )

        return categorized

    def _format_module(self, category_name: str, operations: List[Operation]) -> str:
        """Format a single module's documentation.

        Args:
            category_name: Category name
            operations: List of operations in this category

        Returns:
            Formatted documentation string
        """
        category_config = self.config.get_category(category_name)
        sdk_display = self.version_config.display_name

        # Format system prompt with SDK name
        system_prompt = category_config.system_prompt.format(sdk_name=sdk_display)

        doc = f"""<SYSTEM>{system_prompt}</SYSTEM>

# {sdk_display} {category_config.title} Documentation

{category_config.description}

"""

        # Format each operation
        section_num = 1
        for operation in operations:
            doc += self._format_operation(operation, section_num)
            section_num += 1

        return doc

    def _format_operation(self, operation: Operation, section_num: int) -> str:
        """Format a single operation with all its examples.

        Args:
            operation: Operation to format
            section_num: Section number

        Returns:
            Formatted operation string
        """
        doc = f"# {section_num}. {operation.title}\n\n"

        # Add description if present
        if operation.description:
            doc += f"{operation.description}\n\n"

        # Add notes if present
        if operation.notes:
            doc += f"{operation.notes}\n\n"

        # Add all examples
        if operation.examples:
            for idx, example in enumerate(operation.examples, 1):
                doc += self._format_example(example, section_num, idx)

        return doc

    def _format_example(self, example: Example, section_num: int, example_num: int) -> str:
        """Format a single code example with inline SQL/JSON for context optimization.

        Args:
            example: Example to format
            section_num: Section number
            example_num: Example number within section

        Returns:
            Formatted example string
        """
        doc = f"## {section_num}.{example_num}. {example.name}\n\n"

        # Single code block with inline SQL/JSON comments for context optimization
        if example.code:
            doc += f"{example.code}\n"

            # Inline Data Source within code block
            if example.data_sql:
                # Remove markdown code fences if present
                clean_sql = example.data_sql.replace("```sql", "").replace("```", "").strip()
                doc += f"\n// Data Source\n/*\n{clean_sql}\n*/\n"

            # Inline Response within code block
            if example.response:
                # Remove markdown code fences if present
                clean_response = (
                    example.response.replace("```json", "").replace("```", "").strip()
                )
                doc += f"\n// Response\n/*\n{clean_response}\n*/\n"

            doc += "```\n"

        # Description/Note outside code block
        if example.description:
            doc += f"\n// Note: {example.description}\n"

        doc += "\n"
        return doc

    def _write_module_file(self, output_dir: Path, category_name: str, content: str) -> None:
        """Write module documentation to file.

        Args:
            output_dir: Output directory
            category_name: Category name
            content: Documentation content
        """
        filename_prefix = self.version_config.output.filename_prefix
        filename = f"{filename_prefix}-{category_name}-llms.txt"
        filepath = output_dir / filename

        filepath.write_text(content, encoding="utf-8")
        logger.info(f"Generated {filename}")

    def _generate_full_doc(self, output_dir: Path, module_contents: Dict[str, str]) -> None:
        """Generate combined documentation with all modules.

        Args:
            output_dir: Output directory
            module_contents: Dictionary of module contents
        """
        sdk_display = self.version_config.display_name

        full_doc = f"""<SYSTEM>This is the complete developer documentation for {sdk_display}.</SYSTEM>

# {sdk_display} - Complete Documentation

Complete reference for {sdk_display} covering all modules.

"""

        # Combine all module contents in order
        for category_name, category_config in self.config.get_sorted_categories():
            if category_name in module_contents:
                content = module_contents[category_name]
                # Remove the module's system prompt and header for combined doc
                lines = content.split("\n")
                # Skip system tag, blank, title, blank, description
                content_without_header = "\n".join(lines[5:])
                full_doc += content_without_header + "\n\n"

        # Write full documentation
        filename_prefix = self.version_config.output.filename_prefix
        filename = f"{filename_prefix}-full-llms.txt"
        filepath = output_dir / filename
        filepath.write_text(full_doc, encoding="utf-8")
        logger.info(f"Generated {filename}")
