"""HTTP fetching utilities for downloading specifications."""

import logging
import requests
from pathlib import Path
from typing import Optional

from ..config.loader import ConfigLoader

logger = logging.getLogger(__name__)


def fetch_spec(
    sdk_name: str,
    version: str,
    config: ConfigLoader,
    force_download: bool = False
) -> Path:
    """Fetch specification file for SDK version.

    Args:
        sdk_name: Name of the SDK (e.g., 'swift', 'dart', 'javascript')
        version: Version string (e.g., 'v2', 'latest')
        config: ConfigLoader instance
        force_download: Force download even if local file exists

    Returns:
        Path to the specification file

    Raises:
        requests.RequestException: If download fails
    """
    version_config = config.get_sdk_version(sdk_name, version)

    # Resolve 'latest' to actual version
    if version == "latest":
        sdk = config.get_sdk(sdk_name)
        version = sdk.get_latest_version()

    # Check if local path is specified and exists
    if version_config.spec.local_path and not force_download:
        local_path = Path(version_config.spec.local_path)
        if local_path.exists():
            logger.info(f"Using local spec file: {local_path}")
            return local_path

    # Download from URL
    spec_url = version_config.spec.url
    logger.info(f"Fetching spec from: {spec_url}")

    try:
        response = requests.get(spec_url, timeout=30)
        response.raise_for_status()

        # Save to config directory with versioned filename
        filename = f"supabase_{sdk_name}_{version}.yml"
        output_path = Path("config") / filename
        output_path.parent.mkdir(parents=True, exist_ok=True)

        with open(output_path, "w", encoding="utf-8") as f:
            f.write(response.text)

        logger.info(f"Spec downloaded to: {output_path}")
        return output_path

    except requests.RequestException as e:
        logger.error(f"Failed to fetch spec from {spec_url}: {e}")
        raise


def download_file(url: str, output_path: Path) -> None:
    """Download a file from URL to local path.

    Args:
        url: URL to download from
        output_path: Local path to save file

    Raises:
        requests.RequestException: If download fails
    """
    logger.debug(f"Downloading from {url} to {output_path}")

    response = requests.get(url, timeout=30)
    response.raise_for_status()

    output_path.parent.mkdir(parents=True, exist_ok=True)
    with open(output_path, "wb") as f:
        f.write(response.content)

    logger.debug(f"Downloaded successfully to {output_path}")
