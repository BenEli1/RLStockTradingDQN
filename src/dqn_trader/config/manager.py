"""Configuration loading and validation."""

from dataclasses import dataclass
from pathlib import Path
from typing import Any

import yaml


@dataclass(frozen=True)
class ConfigManager:
    """Loads versioned YAML configuration files."""

    config_path: Path = Path("config/setup.yaml")

    def load(self) -> dict[str, Any]:
        with self.config_path.open("r", encoding="utf-8") as handle:
            config = yaml.safe_load(handle)
        if config.get("version") != "1.00":
            raise ValueError("Unsupported setup configuration version")
        return config

    def section(self, name: str) -> dict[str, Any]:
        config = self.load()
        if name not in config:
            raise KeyError(f"Missing configuration section: {name}")
        return config[name]
