import json
import logging
import os
from datetime import datetime
from typing import Any, Dict, Optional

from synapse.module_api import ModuleApi

logger = logging.getLogger(__name__)

class MessageLogger:
    def __init__(self, config: Dict[str, Any], api: ModuleApi):
        self.api = api
        self.log_file = config.get("log_file", "/var/log/synapse/messages.json")
        self.api.register_room_message_handler(self.on_room_message)

    @staticmethod
    def parse_config(config: Dict[str, Any]) -> Dict[str, Any]:
        """Parse the module configuration."""
        log_file = config.get("log_file", "/var/log/synapse/messages.json")
        # Ensure the directory exists
        os.makedirs(os.path.dirname(log_file), exist_ok=True)
        return {"log_file": log_file}

    async def on_room_message(
        self,
        event: Dict[str, Any],
        ephemeral: bool,
        redacted: bool,
        redacted_by: Optional[str],
    ) -> None:
        """Handle incoming room messages and log them to a JSON file."""
        if event.get("type") != "m.room.message" or redacted:
            return

        message_data = {
            "event_id": event.get("event_id"),
            "room_id": event.get("room_id"),
            "sender": event.get("sender"),
            "timestamp": datetime.fromtimestamp(event.get("origin_server_ts", 0) / 1000.0).isoformat(),
            "content": event.get("content", {}),
        }

        try:
            # Append to JSON file
            with open(self.log_file, "a", encoding="utf-8") as f:
                json.dump(message_data, f, ensure_ascii=False)
                f.write("\n")  # Newline for JSON Lines format
        except Exception as e:
            logger.error(f"Failed to log message to {self.log_file}: {e}")

def setup_module(api: ModuleApi, config: Dict[str, Any]) -> MessageLogger:
    """Initialize the module."""
    return MessageLogger(config, api)
