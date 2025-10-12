"""Pydantic schemas for configuration validation."""

from typing import Dict, List, Optional
from pydantic import BaseModel, Field


class SpecConfig(BaseModel):
    """Specification source configuration."""

    url: str
    local_path: Optional[str] = None
    format: str = "openref-0.1"


class OutputConfig(BaseModel):
    """Output directory and file naming configuration."""

    base_dir: str
    filename_prefix: str


class SDKVersionConfig(BaseModel):
    """Configuration for a specific SDK version."""

    display_name: str
    spec: SpecConfig
    output: OutputConfig


class SDKConfig(BaseModel):
    """SDK-specific configuration with multi-version support."""

    name: str
    language: str
    versions: Dict[str, SDKVersionConfig]

    def get_version(self, version: str) -> Optional[SDKVersionConfig]:
        """Get configuration for a specific version."""
        return self.versions.get(version)

    def get_latest_version(self) -> str:
        """Get the latest version key (highest version number)."""
        version_keys = list(self.versions.keys())
        if not version_keys:
            raise ValueError(f"No versions available for SDK {self.name}")

        # Sort versions (v3, v2, v1, v0)
        sorted_versions = sorted(
            version_keys,
            key=lambda v: int(v.replace('v', '')),
            reverse=True
        )
        return sorted_versions[0]

    def get_all_versions(self) -> List[str]:
        """Get all available version keys."""
        return list(self.versions.keys())


class CategoryConfig(BaseModel):
    """Documentation category configuration."""

    title: str
    description: str
    system_prompt: str
    operations: List[str] = Field(default_factory=list)
    order: int
