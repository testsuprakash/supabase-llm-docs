"""Configuration loader for SDK and category definitions."""

import yaml
from pathlib import Path
from typing import Dict, List, Optional, Tuple
from .schemas import SDKConfig, SDKVersionConfig, CategoryConfig


class ConfigLoader:
    """Load and validate configuration files."""

    def __init__(self, config_dir: Path):
        """Initialize configuration loader.

        Args:
            config_dir: Path to configuration directory containing sdks.yaml and categories.yaml
        """
        self.config_dir = Path(config_dir)
        self._sdks: Dict[str, SDKConfig] = {}
        self._categories: Dict[str, CategoryConfig] = {}
        self._load_configs()

    def _load_configs(self) -> None:
        """Load all configuration files."""
        # Load SDKs
        sdks_path = self.config_dir / "sdks.yaml"
        with open(sdks_path, "r", encoding="utf-8") as f:
            sdk_data = yaml.safe_load(f)
            for sdk_name, config in sdk_data["sdks"].items():
                self._sdks[sdk_name] = SDKConfig(**config)

        # Load categories
        categories_path = self.config_dir / "categories.yaml"
        with open(categories_path, "r", encoding="utf-8") as f:
            category_data = yaml.safe_load(f)
            for name, config in category_data["categories"].items():
                self._categories[name] = CategoryConfig(**config)

    def get_sdk(self, name: str) -> SDKConfig:
        """Get SDK configuration by name.

        Args:
            name: SDK name (e.g., 'swift', 'dart', 'javascript')

        Returns:
            SDKConfig object

        Raises:
            KeyError: If SDK name not found
        """
        if name not in self._sdks:
            raise KeyError(f"SDK '{name}' not found in configuration")
        return self._sdks[name]

    def get_sdk_version(self, sdk_name: str, version: str) -> SDKVersionConfig:
        """Get specific SDK version configuration.

        Args:
            sdk_name: SDK name
            version: Version string (e.g., 'v2', 'latest')

        Returns:
            SDKVersionConfig object

        Raises:
            KeyError: If SDK or version not found
        """
        sdk = self.get_sdk(sdk_name)

        if version == "latest":
            version = sdk.get_latest_version()

        version_config = sdk.get_version(version)
        if version_config is None:
            available = ", ".join(sdk.get_all_versions())
            raise KeyError(
                f"Version '{version}' not found for SDK '{sdk_name}'. "
                f"Available versions: {available}"
            )

        return version_config

    def get_all_sdks(self) -> List[str]:
        """Get list of all configured SDK names.

        Returns:
            List of SDK names
        """
        return list(self._sdks.keys())

    def get_sdk_versions(self, sdk_name: str) -> List[str]:
        """Get all versions for a specific SDK.

        Args:
            sdk_name: SDK name

        Returns:
            List of version strings

        Raises:
            KeyError: If SDK not found
        """
        sdk = self.get_sdk(sdk_name)
        return sdk.get_all_versions()

    def get_all_sdk_version_pairs(self) -> List[Tuple[str, str]]:
        """Get all SDK and version combinations.

        Returns:
            List of (sdk_name, version) tuples
        """
        pairs = []
        for sdk_name in self.get_all_sdks():
            sdk = self.get_sdk(sdk_name)
            for version in sdk.get_all_versions():
                pairs.append((sdk_name, version))
        return pairs

    def get_categories(self) -> Dict[str, CategoryConfig]:
        """Get all category configurations.

        Returns:
            Dictionary mapping category names to CategoryConfig objects
        """
        return self._categories

    def get_category(self, name: str) -> CategoryConfig:
        """Get specific category configuration.

        Args:
            name: Category name (e.g., 'database', 'auth')

        Returns:
            CategoryConfig object

        Raises:
            KeyError: If category name not found
        """
        if name not in self._categories:
            raise KeyError(f"Category '{name}' not found in configuration")
        return self._categories[name]

    def get_operations_for_category(self, category: str) -> List[str]:
        """Get operation IDs for a category.

        Args:
            category: Category name

        Returns:
            List of operation IDs
        """
        return self._categories[category].operations

    def get_sorted_categories(self) -> List[tuple[str, CategoryConfig]]:
        """Get categories sorted by their order field.

        Returns:
            List of (name, config) tuples sorted by order
        """
        return sorted(self._categories.items(), key=lambda x: x[1].order)
