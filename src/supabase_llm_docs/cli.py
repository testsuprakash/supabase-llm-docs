"""Command-line interface for Supabase documentation generator."""

import click
import logging
from pathlib import Path
from rich.console import Console
from rich.progress import track

from .core.parser import OpenRefParser
from .core.formatter import LLMFormatter
from .config.loader import ConfigLoader
from .utils.logger import setup_logger
from .utils.fetcher import fetch_spec

console = Console()


@click.group()
@click.version_option(version="1.0.0")
def cli():
    """Supabase Documentation Generator for LLMs.

    Generate LLM-optimized documentation from Supabase SDK specifications.
    """
    pass


@cli.command()
@click.option(
    "--sdk",
    help="SDK to generate docs for (e.g., javascript, swift, kotlin, or 'all' for all SDKs)",
)
@click.option(
    "--version",
    default="latest",
    help="Version to generate (e.g., v2, v1, 'latest' for newest version, or 'all' for all versions)",
)
@click.option(
    "--config-dir",
    type=click.Path(exists=True, path_type=Path),
    default=Path("config"),
    help="Configuration directory",
)
@click.option(
    "--output-dir",
    type=click.Path(path_type=Path),
    default=Path("output"),
    help="Output directory",
)
@click.option("--verbose", "-v", is_flag=True, help="Enable verbose logging")
def generate(
    sdk: str,
    version: str,
    config_dir: Path,
    output_dir: Path,
    verbose: bool
):
    """Generate LLM documentation for specified SDK(s) and version(s)."""

    # Setup logging
    log_level = "DEBUG" if verbose else "INFO"
    setup_logger(level=log_level)
    logger = logging.getLogger(__name__)

    console.print("[bold blue]Supabase LLM Documentation Generator[/bold blue]")
    console.print()

    try:
        # Load configuration
        config = ConfigLoader(config_dir)

        # Validate SDK input
        available_sdks = config.get_all_sdks()
        if not sdk:
            console.print("[bold red]Error: --sdk is required[/bold red]")
            console.print(f"Available SDKs: {', '.join(available_sdks)}")
            raise click.Abort()

        # Determine which SDKs to process
        if sdk == "all":
            sdks_to_process = available_sdks
        else:
            if sdk not in available_sdks:
                console.print(f"[bold red]Error: SDK '{sdk}' not found[/bold red]")
                console.print(f"Available SDKs: {', '.join(available_sdks)}")
                raise click.Abort()
            sdks_to_process = [sdk]

        # Build list of (sdk, version) pairs to process
        tasks = []
        for sdk_name in sdks_to_process:
            if version == "all":
                versions = config.get_sdk_versions(sdk_name)
                for v in versions:
                    tasks.append((sdk_name, v))
            else:
                tasks.append((sdk_name, version))

        # Process each SDK/version combination
        for sdk_name, ver in track(
            tasks, description="[cyan]Processing...", console=console
        ):
            console.print(f"\n[green]Processing {sdk_name} {ver}...[/green]")

            try:
                # Fetch spec
                spec_path = fetch_spec(sdk_name, ver, config)

                # Parse spec
                parser = OpenRefParser(spec_path)
                parsed_data = parser.parse()

                # Save parsed JSON with versioned path
                sdk_version_dir = output_dir / sdk_name / ver
                parsed_dir = sdk_version_dir / "parsed"
                parsed_dir.mkdir(parents=True, exist_ok=True)
                parsed_json = parsed_dir / f"{sdk_name}-{ver}-spec.json"
                parser.save_json(parsed_data, parsed_json)

                # Format for LLM
                llm_docs_dir = sdk_version_dir / "llm-docs"
                llm_docs_dir.mkdir(parents=True, exist_ok=True)
                formatter = LLMFormatter(parsed_data, config, sdk_name, ver)
                formatter.generate_all(sdk_version_dir)

                console.print(f"[green]  Completed {sdk_name} {ver}[/green]")

            except Exception as e:
                logger.error(
                    f"Error processing {sdk_name} {ver}: {e}",
                    exc_info=verbose
                )
                console.print(f"[red]  Failed {sdk_name} {ver}: {e}[/red]")
                if len(tasks) > 1:
                    continue  # Continue with other SDK/version pairs
                else:
                    raise

        console.print("\n[bold green]Generation complete![/bold green]")
        console.print(f"\nOutput location: {output_dir.absolute()}")

    except Exception as e:
        logger.error(f"Fatal error: {e}", exc_info=True)
        console.print(f"\n[bold red]Error: {e}[/bold red]")
        raise click.Abort()


@cli.command()
@click.argument("sdk")
@click.option(
    "--version",
    default="latest",
    help="Version to validate (default: latest)",
)
@click.option(
    "--config-dir",
    type=click.Path(exists=True, path_type=Path),
    default=Path("config"),
    help="Configuration directory",
)
def validate(sdk: str, version: str, config_dir: Path):
    """Validate SDK specification."""
    console.print(f"[yellow]Validating {sdk} {version} specification...[/yellow]")

    try:
        # Load configuration
        config = ConfigLoader(config_dir)

        # Fetch and parse spec
        spec_path = fetch_spec(sdk, version, config)
        parser = OpenRefParser(spec_path)
        parsed_data = parser.parse()

        console.print(f"\n[green]Validation successful![/green]")
        console.print(f"  SDK: {sdk}")
        console.print(f"  Version: {version}")
        console.print(f"  Operations: {len(parsed_data.operations)}")
        console.print(f"  Examples: {parsed_data.total_examples}")

    except Exception as e:
        console.print(f"\n[red]Validation failed: {e}[/red]")
        raise click.Abort()


@cli.command()
@click.option(
    "--config-dir",
    type=click.Path(exists=True, path_type=Path),
    default=Path("config"),
    help="Configuration directory",
)
def list_sdks(config_dir: Path):
    """List all configured SDKs and their versions."""
    console.print("[bold]Configured SDKs:[/bold]\n")

    try:
        config = ConfigLoader(config_dir)

        for sdk_name in config.get_all_sdks():
            sdk_config = config.get_sdk(sdk_name)
            console.print(f"  [cyan]{sdk_name}[/cyan]")
            console.print(f"    Name: {sdk_config.name}")
            console.print(f"    Language: {sdk_config.language}")

            versions = sdk_config.get_all_versions()
            console.print(f"    Versions: {', '.join(versions)}")

            # Show details for each version
            for ver in versions:
                ver_config = sdk_config.get_version(ver)
                console.print(f"      {ver}:")
                console.print(f"        Display: {ver_config.display_name}")
                console.print(f"        Spec: {ver_config.spec.url}")

            console.print()

    except Exception as e:
        console.print(f"[red]Error loading configuration: {e}[/red]")
        raise click.Abort()


def main():
    """Entry point for CLI."""
    cli()


if __name__ == "__main__":
    main()
