"""Tests for the configuration functionality.

This module contains tests for the Configuration class that handles
loading and providing access to the application configuration.
"""
import os
import pytest
import tempfile
from unittest.mock import patch
from pylogger_slack._config import Configuration

class TestConfiguration:
    """Test suite for the Configuration class."""
    
    def test_default_config(self):
        """Test that default configuration is loaded correctly."""
        config = Configuration().config
        assert config["disable_existing_loggers"] is False
        assert "formatters" in config
        assert "handlers" in config
        assert "root" in config
    
    def test_custom_config_loading(self):
        """Test loading custom configuration from a file."""
        with tempfile.NamedTemporaryFile(suffix=".toml", delete=False) as temp_file:
            temp_file.write(b"""
            disable_existing_loggers = true
            slack_webhook_url = "https://hooks.slack.com/test/webhook"
            dev = false
            format_type = "json"
            
            [formatters.custom]
            format = "%(asctime)s - TEST - %(message)s"
            """)
            temp_file_path = temp_file.name
        
        try:
            # Mock the _read_config method to return our temporary file's content
            with patch.object(Configuration, '_read_config') as mock_read:
                from tomllib import load
                with open(temp_file_path, "rb") as f:
                    mock_read.return_value = load(f)
                
                config = Configuration().config
                assert config["disable_existing_loggers"] is True
                assert config["slack_webhook_url"] == "https://hooks.slack.com/test/webhook"
                assert config["dev"] is False
                assert config["format_type"] == "json"
                assert "custom" in config["formatters"]
                assert config["formatters"]["custom"]["format"] == "%(asctime)s - TEST - %(message)s"
        finally:
            # Clean up
            os.unlink(temp_file_path)
    
    def test_yaml_format_config(self):
        """Test loading configuration with YAML format type."""
        with tempfile.NamedTemporaryFile(suffix=".toml", delete=False) as temp_file:
            temp_file.write(b"""
            disable_existing_loggers = false
            slack_webhook_url = "https://hooks.slack.com/test/webhook"
            dev = true
            format_type = "yaml"
            
            [formatters.yaml_fmt]
            format = "%(asctime)s - %(levelname)s - %(message)s"
            extra = { "environment" = "testing", "app" = "test_app" }
            """)
            temp_file_path = temp_file.name
        
        try:
            # Mock the _read_config method to return our temporary file's content
            with patch.object(Configuration, '_read_config') as mock_read:
                from tomllib import load
                with open(temp_file_path, "rb") as f:
                    mock_read.return_value = load(f)
                
                config = Configuration().config
                assert config["disable_existing_loggers"] is False
                assert config["format_type"] == "yaml"
                assert "yaml_fmt" in config["formatters"]
                assert config["formatters"]["yaml_fmt"]["format"] == "%(asctime)s - %(levelname)s - %(message)s"
                assert config["formatters"]["yaml_fmt"]["extra"]["environment"] == "testing"
                assert config["formatters"]["yaml_fmt"]["extra"]["app"] == "test_app"
        finally:
            # Clean up
            os.unlink(temp_file_path)
    
    def test_default_format_config(self):
        """Test loading configuration with default format type."""
        with tempfile.NamedTemporaryFile(suffix=".toml", delete=False) as temp_file:
            temp_file.write(b"""
            disable_existing_loggers = false
            slack_webhook_url = "https://hooks.slack.com/test/webhook"
            dev = true
            format_type = "default"
            
            [formatters.plain]
            format = "%(levelname)s: %(message)s"
            datefmt = "%Y-%m-%d"
            """)
            temp_file_path = temp_file.name
        
        try:
            # Mock the _read_config method to return our temporary file's content
            with patch.object(Configuration, '_read_config') as mock_read:
                from tomllib import load
                with open(temp_file_path, "rb") as f:
                    mock_read.return_value = load(f)
                
                config = Configuration().config
                assert config["format_type"] == "default"
                assert "plain" in config["formatters"]
                assert config["formatters"]["plain"]["format"] == "%(levelname)s: %(message)s"
                assert config["formatters"]["plain"]["datefmt"] == "%Y-%m-%d"
        finally:
            # Clean up
            os.unlink(temp_file_path)
    
    def test_deep_merge(self):
        """Test the deep merge functionality."""
        config = Configuration()
        
        default = {
            "a": 1,
            "b": {"x": 10, "y": 20},
            "c": [1, 2]
        }
        
        override = {
            "a": 5,
            "b": {"y": 30, "z": 40},
            "d": "new"
        }
        
        result = config._deep_merge(default, override)
        
        assert result["a"] == 5  # Completely overridden
        assert result["b"]["x"] == 10  # Kept from default
        assert result["b"]["y"] == 30  # Overridden in nested dict
        assert result["b"]["z"] == 40  # Added to nested dict
        assert result["c"] == [1, 2]  # Kept from default
        assert result["d"] == "new"  # Added from override
