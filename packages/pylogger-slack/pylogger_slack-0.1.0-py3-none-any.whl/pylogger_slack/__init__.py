"""
PyLogger-Slack: Python logging with formatting options and Slack notifications.

This package provides enhanced logging capabilities with YAML/JSON formatting
and integrated Slack notifications for monitoring applications in production.
"""

from pylogger_slack._config import Configuration
from pylogger_slack.logger import (LoggerInitializer)
from pylogger_slack.slack import SlackNotification
import logging

__version__ = "0.1.0"
CONFIG = Configuration().config

LOGGER = logging.getLogger(__name__)
initializer = LoggerInitializer()
initializer(logger=LOGGER)

SLACK = SlackNotification()

__all__ = [
    "LOGGER", 
    "SLACK", 
    "CONFIG",
    "__version__"
]