"""
Tests for the Slack notification functionality.
"""
import pytest
from unittest.mock import patch, MagicMock
from pylogger_slack.slack import SlackNotification


class TestSlackNotification:
    
    def test_init_with_webhook(self):
        """Test initialization with explicit webhook URL."""
        webhook_url = "https://hooks.slack.com/test/webhook"
        
        with patch("pylogger_slack.CONFIG", {}):
            notification = SlackNotification(webhook=webhook_url, dev=False)
            assert notification._webhook == webhook_url
            assert notification._dev is False
    
    def test_init_from_config(self):
        """Test initialization from configuration."""
        config_webhook = "https://hooks.slack.com/config/webhook"
        
        with patch("pylogger_slack.CONFIG", {
            "slack_webhook_url": config_webhook,
            "dev": False
        }):
            notification = SlackNotification()
            assert notification._webhook == config_webhook
            assert notification._dev is False
    
    def test_init_from_env_var(self):
        """Test initialization from environment variable."""
        env_webhook = "https://hooks.slack.com/env/webhook"
        
        with patch("pylogger_slack.CONFIG", {}):
            with patch("os.getenv", return_value=env_webhook):
                notification = SlackNotification(dev=False)
                assert notification._webhook == env_webhook
    
    def test_notify_dev_mode(self):
        """Test notify in dev mode (printing instead of sending)."""
        with patch("pylogger_slack.CONFIG", {}):
            notification = SlackNotification(dev=True)
            
            with patch("builtins.print") as mock_print:
                notification.notify("Test message")
                
                mock_print.assert_called_once()
                args, _ = mock_print.call_args
                assert "Test message" in args[0]
    
    def test_notify_with_slack_sdk(self):
        """Test notify with slack_sdk integration."""
        webhook_url = "https://hooks.slack.com/test/webhook"
        
        mock_client = MagicMock()
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_client.send.return_value = mock_response
        
        with patch("pylogger_slack.CONFIG", {}):
            notification = SlackNotification(webhook=webhook_url, dev=False)
            
            with patch("slack_sdk.WebhookClient", return_value=mock_client):
                result = notification.notify("Test message")
                
                assert result is True
                mock_client.send.assert_called_once()
    
    def test_notify_with_extra_fields(self):
        """Test notify with extra fields."""
        webhook_url = "https://hooks.slack.com/test/webhook"
        
        mock_client = MagicMock()
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_client.send.return_value = mock_response
        
        with patch("pylogger_slack.CONFIG", {}):
            notification = SlackNotification(webhook=webhook_url, dev=False)
            
            with patch("slack_sdk.WebhookClient", return_value=mock_client):
                extra_fields = {"field1": "value1", "field2": "value2"}
                notification.notify("Test message", extra_fields=extra_fields)
                
                mock_client.send.assert_called_once()
                
                _, kwargs = mock_client.send.call_args
                blocks = kwargs.get("blocks", [])
                
                fields_found = False
                for block in blocks:
                    if block.get("type") == "section" and "fields" in block:
                        for field in block["fields"]:
                            if "*field1*" in field.get("text", "") or "*field2*" in field.get("text", ""):
                                fields_found = True
                
                assert fields_found, "Extra fields were not included in the blocks"
    
    def test_notify_with_custom_blocks(self):
        """Test notify with custom blocks."""
        webhook_url = "https://hooks.slack.com/test/webhook"
        
        mock_client = MagicMock()
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_client.send.return_value = mock_response
        
        with patch("pylogger_slack.CONFIG", {}):
            notification = SlackNotification(webhook=webhook_url, dev=False)
            
            with patch("slack_sdk.WebhookClient", return_value=mock_client):
                custom_blocks = [
                    {"type": "header", "text": {"type": "plain_text", "text": "Custom Header"}}
                ]
                
                notification.notify("Test message", blocks=custom_blocks)
                
                _, kwargs = mock_client.send.call_args
                assert kwargs.get("blocks") == custom_blocks
    
    def test_notify_error_handling(self):
        """Test error handling during notification."""
        webhook_url = "https://hooks.slack.com/test/webhook"
        
        with patch("pylogger_slack.CONFIG", {}):
            notification = SlackNotification(webhook=webhook_url, dev=False)
            
            with patch("slack_sdk.WebhookClient", side_effect=ImportError()):
                with patch("warnings.warn") as mock_warn:
                    result = notification.notify("Test message")
                    
                    assert result is False
                    mock_warn.assert_called_once()
                    args, _ = mock_warn.call_args
                    assert "slack_sdk required" in args[0]
            
            with patch("slack_sdk.WebhookClient", side_effect=Exception("Test error")):
                with patch("warnings.warn") as mock_warn:
                    result = notification.notify("Test message")
                    
                    assert result is False
                    mock_warn.assert_called_once()
                    args, _ = mock_warn.call_args
                    assert "Test error" in args[0]
