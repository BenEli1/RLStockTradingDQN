import pytest

from dqn_trader.config.manager import ConfigManager


def test_config_loads_versioned_file(config_file):
    config = ConfigManager(config_file).load()
    assert config["section"]["value"] == 3


def test_config_returns_existing_section(config_file):
    assert ConfigManager(config_file).section("section") == {"value": 3}


def test_config_missing_section_raises(config_file):
    with pytest.raises(KeyError):
        ConfigManager(config_file).section("missing")


def test_config_rejects_unsupported_version(tmp_path):
    config = tmp_path / "setup.yaml"
    config.write_text('version: "0.99"\nsection: {}\n', encoding="utf-8")
    with pytest.raises(ValueError, match="Unsupported"):
        ConfigManager(config).load()
