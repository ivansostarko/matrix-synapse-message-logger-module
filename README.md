# Matrix Synapse Message Logger Module

This Synapse module logs all room messages (`m.room.message` events) to a JSON Lines file, capturing details such as event ID, room ID, sender, timestamp, and message content. It is designed to be lightweight, easy to configure, and compatible with Synapse's module API.

## Features
- Logs all non-redacted room messages to a specified JSON file.
- Stores message details in JSON Lines format for easy parsing.
- Configurable log file path.
- Skips redacted messages to avoid logging sensitive or removed content.
- Ensures the log directory is created automatically.

## Requirements
- Matrix Synapse server (version 1.0 or higher).
- Python 3.7 or higher (compatible with Synapse's requirements).
- Write permissions for Synapse to the specified log file directory.

## Installation
1. Clone or download this repository to your Synapse server:
   ```bash
   git clone https://github.com/ivansostarko/matrix-synapse-message-logger-module.git
   ```
2. Copy the `message_logger.py` file to your Synapse modules directory (e.g., `/path/to/synapse/modules/`):
   ```bash
   cp matrix-synapse-message-logger/message_logger.py /path/to/synapse/modules/
   ```
3. Ensure Synapse has write permissions to the directory where logs will be stored (e.g., `/var/log/synapse/`).

## Configuration
Add the module to your Synapse `homeserver.yaml` configuration file:

```yaml
modules:
  - module: message_logger.MessageLogger
    config:
      log_file: "/var/log/synapse/messages.json"
```

- `log_file`: Path to the JSON file where messages will be logged. Defaults to `/var/log/synapse/messages.json` if not specified.
- Ensure the directory (e.g., `/var/log/synapse/`) exists and is writable by the Synapse process.

## Usage
1. Restart your Synapse server to load the module:
   ```bash
   systemctl restart matrix-synapse
   ```
2. The module will automatically start logging all non-redacted `m.room.message` events to the specified file.
3. The log file will contain entries in JSON Lines format, with each line representing a message. Example:
   ```json
   {"event_id": "$event_id", "room_id": "!room_id:matrix.org", "sender": "@user:matrix.org", "timestamp": "2025-09-28T13:50:00.000000", "content": {"body": "Hello, world!", "msgtype": "m.text"}}
   ```

## Log Format
Each log entry is a JSON object with the following fields:
- `event_id`: Unique ID of the message event.
- `room_id`: ID of the room where the message was sent.
- `sender`: Matrix user ID of the message sender.
- `timestamp`: ISO 8601 timestamp of when the message was sent.
- `content`: The message content, including the body and message type (e.g., `m.text`).

## Notes
- The module uses the JSON Lines format (one JSON object per line) for efficient appending and parsing.
- Redacted messages are skipped to avoid logging sensitive or removed content.
- If the log file or directory cannot be written to, errors will be logged to Synapse's logging system.

## Troubleshooting
- **Module not loading**: Ensure the module path in `homeserver.yaml` is correct and that `message_logger.py` is in the modules directory.
- **No logs written**: Check that Synapse has write permissions to the log file directory. Verify the `log_file` path is valid.
- **Errors in logs**: Check Synapse logs (e.g., `/var/log/synapse/homeserver.log`) for any exceptions or issues with the module.

## Contributing
Contributions are welcome! Please open an issue or submit a pull request on GitHub.

## License
This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.
