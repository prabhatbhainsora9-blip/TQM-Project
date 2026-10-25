"""
Unit tests for ConfigurationService (Feature 2: Configuration Files).
"""

import os
from services.configuration_service import ConfigurationService, DEFAULT_CONFIG


def test_config_loads_defaults_when_file_missing(temp_config_file: str):
    """Verifies that safe defaults are used when config.json does not exist."""
    if os.path.exists(temp_config_file):
        os.remove(temp_config_file)

    service = ConfigurationService(config_file_path=temp_config_file)
    assert service.get("app_version") == "1.0.0"
    assert service.get("ui.theme") == "Dark"
    assert service.get("logging.log_level") == "INFO"


def test_config_recovers_from_corrupted_json(temp_config_file: str):
    """Verifies safe recovery when config.json has invalid JSON syntax."""
    with open(temp_config_file, "w") as f:
        f.write("{ INVALID JSON CONTENT: 1234,, ")

    service = ConfigurationService(config_file_path=temp_config_file)
    # Must recover with safe defaults rather than crashing
    assert service.get("app_name") == DEFAULT_CONFIG["app_name"]
    assert service.get("ui.scaling") == 1.0


def test_config_get_and_set_dot_notation(config_service: ConfigurationService):
    """Tests nested dot notation get and set accessors."""
    config_service.set("ui.theme", "Light")
    config_service.set("ui.records_per_page", 25)

    assert config_service.get("ui.theme") == "Light"
    assert config_service.get("ui.records_per_page") == 25

    # Test saving
    assert config_service.save() is True

    # Reload from disk
    reloaded = ConfigurationService(config_file_path=config_service.config_file_path)
    assert reloaded.get("ui.theme") == "Light"
    assert reloaded.get("ui.records_per_page") == 25


def test_config_reset_to_defaults(config_service: ConfigurationService):
    """Tests resetting user settings back to factory defaults."""
    config_service.set("ui.theme", "Light")
    assert config_service.reset_to_defaults() is True
    assert config_service.get("ui.theme") == "Dark"
