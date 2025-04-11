"""Logging functionality for the pylogger-slack package.

This module provides classes and utilities for configuring Python's logging system
with enhanced formatting options and integration with Slack notifications.
"""
import http.client
import logging
import logging.config
from functools import partial
from typing import Optional
import warnings
import ecs_logging
import json
import yaml

class LoggerFormatter(logging.Formatter):
    """Custom formatter for log messages with support for multiple output formats."""
    
    def __init__(self, format, datefmt=None, extra=None, exclude_fields=None):
        """
        Initialize a custom logger formatter.
        
        Args:
            format: The log format string
            datefmt: Optional date format string
            extra: Optional dict of extra fields to include in all logs
            exclude_fields: Optional list of field names to exclude from logs
        """
        super().__init__(fmt=format, datefmt=datefmt)
        self.default_extra = extra or {}
        self.exclude_fields = exclude_fields or []

    def format(self, record):
        """
        Format log records according to the configured format type.
        
        Args:
            record: The log record to format
        
        Returns:
            The formatted log message as a string
        """
        from pylogger_slack import CONFIG
        format_type = CONFIG.get("format_type", "default")
        
        base_message = super().format(record)

        extra = record.extra if hasattr(record, "extra") else {}
        combined_extra = {**self.default_extra, **extra}
        filtered_extra = {k: v for k, v in combined_extra.items() if k not in self.exclude_fields}

        if format_type == "yaml":
            return yaml.dump({"log": base_message, "extra": filtered_extra})
        elif format_type == "json":
            return json.dumps({"log": base_message, "extra": filtered_extra})
        return base_message


class LoggerInitializer:
    """Initializer for configuring loggers with the pylogger-slack settings."""
    
    def __call__(self, logger: logging.Logger, name: Optional[str] = None):
        """
        Configure a logger instance with pylogger-slack settings.
        
        Args:
            logger: The logger instance to configure
            name: Optional name for the logger (defaults to current logger name)
        """
        from pylogger_slack import CONFIG
        self.config = CONFIG
        
        logger.name = name if name else logger.name if logger.name != "__main__" else __name__
        self._apply_config(logger)
        
        http.client.HTTPConnection.debuglevel = 1
        http.client.print = partial(self._print_to_log, logger)

    def _apply_config(self, logger: logging.Logger):
        """
        Apply configuration settings to the logger.
        
        Args:
            logger: The logger instance to configure
        """
        try:
            logging.config.dictConfig(self.config)
        except Exception as e:
            warnings.warn(f"Failed to apply logger config: {e}")

    def _print_to_log(self, logger: logging.Logger, *args, **kwargs):
        """
        Convert HTTP client debug output to structured log entries.
        
        Args:
            logger: The logger to send messages to
            *args, **kwargs: Arguments from HTTP client debug calls
        """
        k = ".".join(str(arg) for arg in args[:-1])
        v = str(args[-1])
        extra = ecs_logging._utils.de_dot(k, v)
        extra.update(kwargs)
        extra.update({"type": "access-log"})
        logger.debug("HTTP log", extra={"extra": extra})