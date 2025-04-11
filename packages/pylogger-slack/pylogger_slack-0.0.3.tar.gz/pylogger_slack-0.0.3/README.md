# pylogger_slack

A Python logging utility with Slack notification support, built for flexibility and ease of use. `pylogger_slack` provides a customizable logger with structured output options (plain text, JSON, YAML) and integrates with Slack for notifications. It's designed to work out of the box with sensible defaults while allowing deep customization via a TOML configuration file.

**Support my development**

<a href="https://www.buymeacoffee.com/i_binay" target="_blank"><img src="https://cdn.buymeacoffee.com/buttons/v2/default-yellow.png" alt="Buy Me A Coffee" style="height: 30px !important;width: 117px !important;" ></a>

## Installation

Install `pylogger_slack` via pip (assuming it's published to PyPI, or install locally):

```bash
pip install pylogger_slack
```

**Dependencies**:
- `ecs-logging` (for ECS formatting)
- `pyyaml` (for YAML output)
- `slack-sdk` (optional, for Slack notifications)


## Quick Start

Here's a basic example to get started:

```python
# example.py
from pylogger_slack import LOGGER, SLACK

# Log messages
LOGGER.info("This is an info message.")
LOGGER.info("Tagged message", extra={"tag": "v1.0"})

# Send Slack notification
SLACK.notify("Something happened!")
```

## Features

- **Structured Logging**: Output logs in plain text, JSON, or YAML format
- **Extended Logger**: Extends Python's built-in logging.Logger with extra functionality
- **Slack Integration**: Easy-to-use Slack notifications
- **Customizable Configuration**: TOML-based configuration with sensible defaults
- **Environment Variable Support**: Use env vars in your configuration
- **Dev Mode**: Skip sending real Slack notifications during development

## Configuration

`pylogger_slack` can be configured in two ways:
1. Using a `pylogger_slack.toml` file in your project root directory
2. Using a `[tool.pylogger_slack]` section in your `pyproject.toml` file

The package also supports environment variable expansion in configuration values.

### Option 1: Using pylogger_slack.toml

Here's an example configuration in a dedicated `pylogger_slack.toml` file:

```toml
version = 1
disable_existing_loggers = false 
slack_webhook_url = "https://hooks.slack.com/services/T00" 
dev = false   # Set to true during development

# General settings
env = "production"  
format_type = "json"  # Options: "default" (plain), "json", "yaml"

# Formatter configuration
[formatters.default]
"()" = "pylogger_slack.logger.LoggerFormatter"
format = "%(asctime)s [%(levelname)s] %(message)s"
datefmt = "%H:%M:%S"
extra = { "app" = "my_app", "version" = "1.0" }
exclude_fields = ["user_id", "secret"]

# Handler configuration
[handlers.console]
class = "logging.StreamHandler"
level = "INFO"
formatter = "default"
stream = "ext://sys.stdout"

[handlers.file]
class = "logging.FileHandler"
level = "WARNING"
formatter = "default"
filename = "app.log"

# Root logger configuration
[root]
level = "DEBUG"
handlers = ["console", "file"]
```

### Option 2: Using pyproject.toml

Alternatively, you can add your configuration to your existing `pyproject.toml` file using the `[tool.pylogger_slack]` section:

```toml
[build-system]
requires = ["setuptools>=42", "wheel"]
build-backend = "setuptools.build_meta"

[project]
name = "your-project-name"
version = "0.1.0"
# ... other project metadata ...

# pylogger_slack configuration
[tool.pylogger_slack]
version = 1
disable_existing_loggers = false
slack_webhook_url = "https://hooks.slack.com/services/T00"
dev = false
env = "production"
format_type = "json"

[tool.pylogger_slack.formatters.default]
"()" = "pylogger_slack.logger.LoggerFormatter"
format = "%(asctime)s [%(levelname)s] %(message)s"
datefmt = "%H:%M:%S"
extra = { "app" = "my_app", "version" = "1.0" }
exclude_fields = ["user_id", "secret"]

[tool.pylogger_slack.handlers.console]
class = "logging.StreamHandler"
level = "INFO"
formatter = "default"
stream = "ext://sys.stdout"

[tool.pylogger_slack.root]
level = "DEBUG"
handlers = ["console"]
```

## Advanced Usage

### Custom Logger

Create a custom logger with specific name:

```python
import logging
from pylogger_slack.logger import LoggerInitializer

# Create a logger with a specific name
logger = logging.getLogger("my_module")
initializer = LoggerInitializer()
initializer(logger=logger)

logger.info("Message from custom logger")

# Add structured data using the extra parameter
logger.info("User logged in", extra={"user_id": "123", "ip": "192.168.1.1"})
```

### Slack Notifications

The Slack integration provides flexible notification options:

```python
from pylogger_slack import SLACK

# Simple notification
SLACK.notify("Basic notification")

# Notification with extra fields
SLACK.notify(
    "User registered", 
    extra_fields={
        "User ID": "user_123",
        "Time": "2025-04-10 15:30:22",
        "Plan": "Premium"
    }
)

# Custom Slack blocks (advanced)
custom_blocks = [
    {
        "type": "header",
        "text": {"type": "plain_text", "text": "Custom Alert", "emoji": True}
    },
    {
        "type": "section",
        "text": {"type": "mrkdwn", "text": "*Important information*\nSomething needs attention!"}
    }
]
SLACK.notify("Alert message", blocks=custom_blocks)
```

## Local Development

To run the documentation locally:

```bash
# Install MkDocs and required plugins
pip install -e ".[dev]"

# Build and serve documentation
mkdocs serve
```

## Testing

Run the tests using pytest:

```bash
pytest tests/
```

## License

This project is licensed under the GPL-3.0 License - see the LICENSE file for details.
