import pytest

from dqn_trader.config.manager import ConfigManager


def test_config_loads_versioned_file(config_file):
    config = ConfigManager(config_file).load()
    assert config["section"]["value"] == 3


def test_config_missing_section_raises(config_file):
    with pytest.raises(KeyError):
        ConfigManager(config_file).section("missing")
