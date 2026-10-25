"""
Configuration Service for Employee Management System (TQM Edition).
Course: BBAT104 - Fundamentals of Total Quality Management
Student: Prabhat Singh Bhainsora (2410302046)
Quality Goal: Q11 - Improve Maintainability

Implements Feature 2: Configuration Files.
Provides robust configuration loading, fallback defaults, validation,
and persistence without storing sensitive credentials.
"""

import json
import os
import copy
from typing import Any, Dict

DEFAULT_CONFIG: Dict[str, Any] = {
    "app_name": "Employee Management System (TQM Maintainability Edition)",
    "app_version": "1.0.0",
    "academic_info": {
        "student_name": "Prabhat Singh Bhainsora",
        "roll_number": "2410302046",
        "course_code": "BBAT104",
        "course_name": "Fundamentals of Total Quality Management (TQM)",
        "academic_session": "2026-27",
        "branch": "CSE",
        "section": "B",
        "quality_goal": "Q11 - Improve Maintainability"
    },
    "database": {
        "db_path": "data/employee_tqm.db",
        "connection_timeout": 10.0,
        "enable_wal_mode": True
    },
    "logging": {
        "log_dir": "logs",
        "log_file": "logs/application.log",
        "log_level": "INFO",
        "max_bytes": 1048576,
        "backup_count": 5
    },
    "backup": {
        "backup_dir": "backups",
        "auto_backup_on_startup": False,
        "max_backups": 10
    },
    "reports": {
        "output_dir": "reports",
        "default_format": "PDF"
    },
    "ui": {
        "theme": "Dark",
        "accent_color": "blue",
        "scaling": 1.0,
        "records_per_page": 10,
        "confirm_delete": True,
        "enable_toast_notifications": True
    }
}


class ConfigurationService:
    """Manages application configuration with self-healing defaults."""

    def __init__(self, config_file_path: str = "config.json"):
        # Resolve absolute path relative to project root
        self.config_file_path = os.path.abspath(config_file_path)
        self.config_dir = os.path.dirname(self.config_file_path)
        self._config: Dict[str, Any] = copy.deepcopy(DEFAULT_CONFIG)
        self.load()

    def load(self) -> Dict[str, Any]:
        """Loads configuration from JSON file or recovers with safe defaults."""
        if not os.path.exists(self.config_file_path):
            self._config = copy.deepcopy(DEFAULT_CONFIG)
            self.save()
            return self._config

        try:
            with open(self.config_file_path, "r", encoding="utf-8") as f:
                user_config = json.load(f)
                self._config = self._merge_dicts(copy.deepcopy(DEFAULT_CONFIG), user_config)
        except Exception:
            # If JSON is corrupted or unreadable, fall back to safe defaults
            self._config = copy.deepcopy(DEFAULT_CONFIG)
            # Try to safely re-save valid config
            try:
                self.save()
            except Exception:
                pass
        return self._config

    def save(self) -> bool:
        """Persists current configuration to disk."""
        try:
            os.makedirs(os.path.dirname(self.config_file_path), exist_ok=True)
            with open(self.config_file_path, "w", encoding="utf-8") as f:
                json.dump(self._config, f, indent=2)
            return True
        except Exception:
            return False

    def reset_to_defaults(self) -> bool:
        """Resets all settings back to the initial factory defaults."""
        self._config = copy.deepcopy(DEFAULT_CONFIG)
        return self.save()

    def get(self, key_path: str, default: Any = None) -> Any:
        """
        Retrieves a configuration value using dot notation (e.g. 'ui.theme').
        """
        keys = key_path.split(".")
        val = self._config
        for k in keys:
            if isinstance(val, dict) and k in val:
                val = val[k]
            else:
                return default
        return val

    def set(self, key_path: str, value: Any) -> None:
        """Sets a configuration value using dot notation (e.g. 'ui.theme', 'Light')."""
        keys = key_path.split(".")
        target = self._config
        for k in keys[:-1]:
            if k not in target or not isinstance(target[k], dict):
                target[k] = {}
            target = target[k]
        target[keys[-1]] = value

    def get_all(self) -> Dict[str, Any]:
        """Returns a deep copy of the complete configuration dictionary."""
        return copy.deepcopy(self._config)

    @staticmethod
    def _merge_dicts(base: Dict[str, Any], override: Dict[str, Any]) -> Dict[str, Any]:
        """Recursively merges override dictionary into base dictionary."""
        for key, value in override.items():
            if key in base and isinstance(base[key], dict) and isinstance(value, dict):
                base[key] = ConfigurationService._merge_dicts(base[key], value)
            else:
                base[key] = value
        return base
