"""Slack notification functionality for the pylogger-slack package.

This module provides classes and utilities for sending notifications to Slack
channels via webhooks with customizable formatting options.
"""
import os
import warnings
from typing import Any, Dict, Optional
from datetime import datetime


class SlackNotification:
    def __init__(self, webhook: Any = None, dev: bool = None):
        """
        Initialize a Slack notification sender.
        
        Args:
            webhook: Slack webhook URL or None to use from config
            dev: Dev mode flag (True to print instead of sending, None to use from config)
        """
        from pylogger_slack import CONFIG
        self._webhook = (webhook or 
                        CONFIG.get("slack_webhook_url") or 
                        os.getenv("SLACK_WEBHOOK"))
        self._dev = dev if dev is not None else CONFIG.get("dev", True)
        self._env = CONFIG.get("env", "development")
        
        if not self._webhook and not self._dev:
            warnings.warn("Slack Webhook URL required in production mode")

    def notify(self, message: str, blocks: Optional[list] = None, 
              attachments: Optional[list] = None, extra_fields: Optional[Dict] = None):
        """
        Send a notification to Slack.
        
        Args:
            message: The message to send
            blocks: Optional custom blocks for rich formatting
            attachments: Optional attachments to include
            extra_fields: Additional fields to include in the message
        """
        if self._dev:
            print(f"Slack notification (dev mode): {message}")
            if blocks:
                print(f"Blocks: {blocks}")
            if attachments:
                print(f"Attachments: {attachments}")
            if extra_fields:
                print(f"Extra fields: {extra_fields}")
            return
            
        try:
            from slack_sdk import WebhookClient
            webhook = WebhookClient(self._webhook)
            
            message_blocks = blocks or self._create_default_blocks(message, extra_fields)
            
            response = webhook.send(
                text=message,
                blocks=message_blocks,
                attachments=attachments
            )
            
            if response.status_code != 200:
                warnings.warn(f"Slack notification failed: {response.body}")
                return False
            return True
            
        except ImportError:
            warnings.warn("slack_sdk required for notifications: pip install slack-sdk")
            return False
        except Exception as e:
            warnings.warn(f"Slack notification failed: {e}")
            return False
    
    def _create_default_blocks(self, message: str, extra_fields: Optional[Dict] = None) -> list:
        """Create default Slack message blocks with a consistent format."""
        header_emoji = ":information_source:" if self._env == "production" else ":gear:"
        header_text = f"Notification ({self._env})"
        
        blocks = [
            {
                "type": "header",
                "text": {"type": "plain_text", "text": header_text, "emoji": True}
            },
            {
                "type": "section",
                "fields": [
                    {"type": "mrkdwn", "text": "*Type:*\nNotification"},
                    {"type": "mrkdwn", "text": f'*Timestamp:*\n{datetime.now().strftime("%m/%d/%Y, %H:%M:%S")}'}
                ]
            },
            {
                "type": "section",
                "text": {"type": "mrkdwn", "text": f"*Message*\n{message}"}
            }
        ]
        
        if extra_fields:
            fields_block = {
                "type": "section",
                "fields": []
            }
            
            for key, value in extra_fields.items():
                fields_block["fields"].append({
                    "type": "mrkdwn",
                    "text": f"*{key}*\n{value}"
                })
            
            blocks.append(fields_block)
            
        blocks.append({"type": "divider"})
        
        return blocks