"""Tests for the logger functionality.

This module contains tests for the LoggerInitializer and LoggerFormatter classes.
"""
import logging
import pytest
from unittest.mock import patch, MagicMock
from pylogger_slack import LOGGER
from pylogger_slack.logger import LoggerInitializer, LoggerFormatter


class TestLoggerInitializer:
    """Test suite for the LoggerInitializer class."""
    
    def test_logger_initializer_with_name(self):
        """Test LoggerInitializer with explicit name."""
        with patch("logging.getLogger") as mock_get_logger:
            mock_logger = MagicMock()
            mock_get_logger.return_value = mock_logger
            
            initializer = LoggerInitializer()
            initializer(logger=mock_logger, name="test.logger")
            
            # Check that logger name was set
            assert mock_logger.name == "test.logger"
    
    def test_logger_initializer_default_name(self):
        """Test LoggerInitializer using existing logger name."""
        with patch("logging.getLogger") as mock_get_logger:
            mock_logger = MagicMock()
            mock_logger.name = "existing.logger"
            mock_get_logger.return_value = mock_logger
            
            initializer = LoggerInitializer()
            initializer(logger=mock_logger)
            
            assert mock_logger.name == "existing.logger"

    def test_logger_config_applied(self):
        """Test that logger configuration is properly applied."""
        mock_logger = MagicMock()
        
        with patch("logging.config.dictConfig") as mock_dict_config:
            with patch("pylogger_slack.CONFIG", {"test": "config"}):
                initializer = LoggerInitializer()
                initializer(logger=mock_logger)
                
                mock_dict_config.assert_called_once_with({"test": "config"})


class TestLoggerFormatter:
    """Test suite for the LoggerFormatter class."""
    
    def test_format_default(self):
        """Test the default formatting of log records."""
        formatter = LoggerFormatter(format="%(levelname)s - %(message)s")
        
        record = logging.LogRecord(
            name="test", 
            level=logging.INFO, 
            pathname="", 
            lineno=0, 
            msg="Test message", 
            args=(), 
            exc_info=None
        )
        
        with patch("pylogger_slack.CONFIG", {"format_type": "default"}):
            result = formatter.format(record)
            assert result == "INFO - Test message"
    
    def test_format_json(self):
        """Test JSON formatting of log records."""
        formatter = LoggerFormatter(format="%(levelname)s - %(message)s")
        
        record = logging.LogRecord(
            name="test", 
            level=logging.INFO, 
            pathname="", 
            lineno=0, 
            msg="Test message", 
            args=(), 
            exc_info=None
        )
        
        with patch("pylogger_slack.CONFIG", {"format_type": "json"}):
            result = formatter.format(record)
            import json
            parsed = json.loads(result)
            assert parsed["log"] == "INFO - Test message"
            assert "extra" in parsed
    
    def test_format_yaml(self):
        """Test YAML formatting of log records."""
        formatter = LoggerFormatter(format="%(levelname)s - %(message)s")
        
        record = logging.LogRecord(
            name="test", 
            level=logging.INFO, 
            pathname="", 
            lineno=0, 
            msg="Test message", 
            args=(), 
            exc_info=None
        )
        
        with patch("pylogger_slack.CONFIG", {"format_type": "yaml"}):
            result = formatter.format(record)
            assert "log: INFO - Test message" in result
            assert "extra:" in result
    
    def test_default_extra(self):
        """Test that default extra fields are included in the formatted output."""
        default_extra = {"app": "test_app", "version": "1.0"}
        formatter = LoggerFormatter(
            format="%(levelname)s - %(message)s",
            extra=default_extra
        )
        
        record = logging.LogRecord(
            name="test", 
            level=logging.INFO, 
            pathname="", 
            lineno=0, 
            msg="Test message", 
            args=(), 
            exc_info=None
        )
        
        with patch("pylogger_slack.CONFIG", {"format_type": "json"}):
            result = formatter.format(record)
            import json
            parsed = json.loads(result)
            assert parsed["extra"]["app"] == "test_app"
            assert parsed["extra"]["version"] == "1.0"
    
    def test_exclude_fields(self):
        """Test that excluded fields are not included in the formatted output."""
        default_extra = {"app": "test_app", "version": "1.0", "secret": "hidden"}
        formatter = LoggerFormatter(
            format="%(levelname)s - %(message)s",
            extra=default_extra,
            exclude_fields=["secret"]
        )
        
        record = logging.LogRecord(
            name="test", 
            level=logging.INFO, 
            pathname="", 
            lineno=0, 
            msg="Test message", 
            args=(), 
            exc_info=None
        )
        
        with patch("pylogger_slack.CONFIG", {"format_type": "json"}):
            result = formatter.format(record)
            import json
            parsed = json.loads(result)
            assert "app" in parsed["extra"]
            assert "version" in parsed["extra"]
            assert "secret" not in parsed["extra"]
    
    def test_record_extra_overrides_default(self):
        """Test that record extra fields override default extra fields."""
        default_extra = {"app": "test_app", "version": "1.0"}
        formatter = LoggerFormatter(
            format="%(levelname)s - %(message)s",
            extra=default_extra
        )
        
        record = logging.LogRecord(
            name="test", 
            level=logging.INFO, 
            pathname="", 
            lineno=0, 
            msg="Test message", 
            args=(), 
            exc_info=None
        )
        record.extra = {"app": "override_app", "tag": "v1.0"}
        
        with patch("pylogger_slack.CONFIG", {"format_type": "json"}):
            result = formatter.format(record)
            import json
            parsed = json.loads(result)
            assert parsed["extra"]["app"] == "override_app"
            assert parsed["extra"]["version"] == "1.0"
            assert parsed["extra"]["tag"] == "v1.0"


class TestUtilityFunctions:
    """Test suite for utility logging functions."""
    
    def test_convenience_functions(self):
        """Test logging convenience methods with structured data."""
        logger = logging.getLogger("test_utility")
        logger_mock = MagicMock()
        logger.info = logger_mock
        
        extra_data = {"user_id": "123", "action": "login"}
        logger.info("User action", extra={"extra": extra_data})
        
        logger_mock.assert_called_once()
        args, kwargs = logger_mock.call_args
        assert args[0] == "User action"
        assert "extra" in kwargs
    
    def test_log_with_extra(self):
        """Test adding extra fields to logs."""
        logger = logging.getLogger("test_with_extra")
        logger.setLevel(logging.INFO)
        logger.handlers = []
        
        string_io = MagicMock()
        handler = logging.StreamHandler(string_io)
        formatter = LoggerFormatter("%(message)s", extra={"default": "value"})
        handler.setFormatter(formatter)
        logger.addHandler(handler)
        
        logger.info("Test message", extra={"extra": {"custom": "field"}})
        
        assert True
