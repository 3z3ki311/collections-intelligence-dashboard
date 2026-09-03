"""General utility functions for the dashboard."""

from pathlib import Path

import yaml


def load_yaml_config(
        file_path: str | Path,
) -> dict:
    """Load a YAML configuration file."""
    path = Path(file_path)

    if not path.exists():
        raise FileNotFoundError(f"Configuration file was not found: {file_path}")

    with path.open(
        "r",
        encoding="utf-8",
    ) as file:
        config = yaml.safe_load(file)

    return config or {}