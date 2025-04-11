"""Configuration management for the pylogger-slack package.

This module handles loading and providing access to configuration settings from
various sources including default values, TOML files, and environment variables.
"""
import os
import tomllib
import warnings
from typing import Dict

_DEFAULT_CONFIG = {
    "version": 1,
    "disable_existing_loggers": False,
    "slack_webhook_url": None,
    "env": os.getenv("ENV", "development"),
    "dev": True,
    "format_type": "default",

    "formatters": {
        "default": {
            "()": "pylogger_slack.logger.LoggerFormatter",
            "format": "%(asctime)s - %(name)s - %(levelname)s - %(message)s",
            "datefmt": "%Y-%m-%d %H:%M:%S",
            "extra": {},
            "exclude_fields": [],
        }
    },
    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
            "level": "INFO",
            "formatter": "default",
            "stream": "ext://sys.stdout",
        }
    },
    "root": {
        "level": "INFO",
        "handlers": ["console"],
    }
}

class Configuration:
    """Configuration manager for pylogger-slack.
    
    Handles loading configuration from TOML files and providing access to settings.
    """
    def __init__(self):
        """Initialize the configuration manager."""
        self._config = None

    @property
    def config(self) -> Dict:
        """Get the configuration dictionary.
        
        Lazily loads configuration from files on first access.
        
        Returns:
            Dict: The complete configuration dictionary
        """
        if self._config is None:
            config = _DEFAULT_CONFIG.copy()
            updated_config = self._read_config()
            if updated_config:
                config = self._deep_merge(config, updated_config)
            self._config = self._expand_vars(config)
        return self._config

    @config.setter
    def config(self, value: Dict):
        """Prevent direct assignment to config property."""
        raise AttributeError("CONFIG is read-only")
    
    def _deep_merge(self, default: Dict, override: Dict) -> Dict:
        """Recursively merge two dictionaries, preserving nested structure.
        
        Args:
            default: The base dictionary
            override: The dictionary with values to override
            
        Returns:
            Dict: The merged dictionary
        """
        result = default.copy()
        for key, value in override.items():
            if key in result and isinstance(result[key], dict) and isinstance(value, dict):
                result[key] = self._deep_merge(result[key], value)
            else:
                result[key] = value
        return result

    def _read_config(self) -> Dict:
        """Read configuration from TOML files.
        
        Looks for dedicated pylogger_slack.toml file or pyproject.toml with
        [tool.pylogger_slack] section.
        
        Returns:
            Dict: The loaded configuration or empty dict if no files found
        """
        config = {}
        config_path = "pylogger_slack.toml"
        pyproject_path = "pyproject.toml"

        if os.path.exists(config_path):
            config = self._load_toml(config_path)
        elif os.path.exists(pyproject_path):
            pyproject_config = self._load_toml(pyproject_path)
            if "tool" in pyproject_config and "pylogger_slack" in pyproject_config["tool"]:
                config = pyproject_config["tool"]["pylogger_slack"]
        return config

    def _load_toml(self, path: str) -> Dict:
        """Load and parse a TOML file.
        
        Args:
            path: Path to the TOML file
            
        Returns:
            Dict: Parsed TOML content or empty dict on error
        """
        try:
            with open(path, "rb") as f:
                return tomllib.load(f)
        except Exception as e:
            warnings.warn(f"Failed to load TOML config from {path}: {e}")
            return {}

    def _expand_vars(self, config_var):
        """Recursively expand environment variables in configuration values.
        
        Args:
            config_var: The configuration value to process
            
        Returns:
            The processed configuration with environment variables expanded
        """
        def expand(value):
            if isinstance(value, str):
                value = os.path.expandvars(value)
                if "$" in value and not value.startswith("$"):
                    warnings.warn(f"Unexpanded env var in: {value}")
            return value

        if isinstance(config_var, dict):
            return {k: self._expand_vars(v) for k, v in config_var.items()}
        return expand(config_var)