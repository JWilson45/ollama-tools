# API Reference

## Overview

The Ollama Tools API provides secure shell command execution and file operations through RESTful endpoints. All endpoints return JSON responses and use standard HTTP status codes.

## Base URL

```
http://localhost:8000
```

## Authentication

Currently, no authentication is required. For production use, consider implementing authentication middleware.

## Common Response Format

All endpoints return JSON responses with the following structure:

```json
{
  "status": "success|error",
  "data": {...},
  "message": "Optional message"
}
```

## Endpoints

### File Operations

#### POST /read_file

Read a UTF-8 text file from the configured base directory.

**Request Body:**
```json
{
  "path": "path/to/file.txt"
}
```

**Response:**
```json
{
  "content": "File contents here..."
}
```

**Error Responses:**
- `400 Bad Request`: Invalid path
- `403 Forbidden`: Access outside base directory
- `404 Not Found`: File not found
- `415 Unsupported Media Type`: Non-UTF-8 file

**Example:**
```bash
curl -X POST "http://localhost:8000/read_file" \
  -H "Content-Type: application/json" \
  -d '{"path": "README.md"}'
```

### Shell Command Execution

**⚠️ SECURITY NOTICE: The immediate execution endpoint has been removed for security reasons.**

All shell commands must now go through the interactive confirmation workflow to ensure user safety.

**Use these secure endpoints instead:**
- **`POST /run_shell_interactive`** - Preview commands and get confirmation request
- **`POST /run_shell_confirmed/{command_id}`** - Execute only confirmed commands

### Interactive Command Confirmation

#### POST /run_shell_interactive

Interactive shell command execution that requires user confirmation. This endpoint is designed to work with Open WebUI's confirmation workflow.

**Request Body:**
```json
{
  "command": "rm -rf /tmp/test"
}
```

**Response:**
```json
{
  "type": "confirmation_required",
  "title": "Command Execution Requires Confirmation",
  "message": "The command 'rm -rf /tmp/test' requires your confirmation before execution.",
  "command_id": "uuid-here",
  "risk_level": "medium",
  "details": {
    "program": "rm",
    "arguments": ["-rf", "/tmp/test"],
    "working_directory": "/Users/jasonwilson/git/ollama-tools",
    "risk_assessment": "This command has medium risk level"
  },
  "next_steps": [
    "Review the command details above",
    "To execute: Use the run_shell_confirmed endpoint with command_id: uuid-here",
    "To cancel: Use the cancel_command endpoint with command_id: uuid-here"
  ],
  "requires_user_action": true
}
```

**Error Responses:**
- `400 Bad Request`: Command validation failed

**Example:**
```bash
curl -X POST "http://localhost:8000/run_shell_interactive" \
  -H "Content-Type: application/json" \
  -d '{"command": "rm -rf /tmp/test"}'
```

#### POST /run_shell_preview

Preview a command and get risk assessment before execution.

**Request Body:**
```json
{
  "command": "rm -rf /tmp/test"
}
```

**Response:**
```json
{
  "command_id": "uuid-here",
  "command": "rm -rf /tmp/test",
  "preview": {
    "program": "rm",
    "arguments": ["-rf", "/tmp/test"],
    "working_directory": "/Users/jasonwilson/git/ollama-tools",
    "risk_level": "medium",
    "estimated_risk": "medium"
  },
  "message": "Command validated. Use /run_shell_confirmed/uuid-here to execute after confirmation.",
  "requires_confirmation": true,
  "status": "pending"
}
```

**Error Responses:**
- `400 Bad Request`: Command validation failed

**Example:**
```bash
curl -X POST "http://localhost:8000/run_shell_preview" \
  -H "Content-Type: application/json" \
  -d '{"command": "rm -rf /tmp/test"}'
```

#### POST /run_shell_confirmed/{command_id}

Execute a previously previewed command after user confirmation.

**Path Parameters:**
- `command_id`: UUID returned from preview endpoint

**Request Body:**
```json
{
  "confirmed": true
}
```

**Response:**
```json
{
  "command_id": "uuid-here",
  "status": "completed",
  "result": {
    "command": "rm -rf /tmp/test",
    "returncode": 0,
    "stdout": "",
    "stderr": ""
  }
}
```

**Error Responses:**
- `404 Not Found`: Command not found
- `410 Gone`: Command has expired
- `500 Internal Server Error`: Execution failed

**Example:**
```bash
curl -X POST "http://localhost:8000/run_shell_confirmed/uuid-here" \
  -H "Content-Type: application/json" \
  -d '{"confirmed": true}'
```

### Command Management

#### GET /pending_commands

List all pending commands that require confirmation.

**Response:**
```json
{
  "pending_commands": [
    {
      "command_id": "uuid-1",
      "command": "rm -rf /tmp/test",
      "timestamp": "2024-01-15T10:30:00",
      "status": "pending",
      "risk_level": "medium"
    }
  ]
}
```

**Example:**
```bash
curl "http://localhost:8000/pending_commands"
```

#### GET /command_status/{command_id}

Get the current status of a specific command.

**Path Parameters:**
- `command_id`: UUID of the command

**Response:**
```json
{
  "command_id": "uuid-here",
  "command": "rm -rf /tmp/test",
  "timestamp": "2024-01-15T10:30:00",
  "status": "completed",
  "risk_level": "medium",
  "result": {
    "command": "rm -rf /tmp/test",
    "returncode": 0,
    "stdout": "",
    "stderr": ""
  }
}
```

**Example:**
```bash
curl "http://localhost:8000/command_status/uuid-here"
```

#### DELETE /cancel_command/{command_id}

Cancel a pending command.

**Path Parameters:**
- `command_id`: UUID of the command to cancel

**Response:**
```json
{
  "command_id": "uuid-here",
  "status": "cancelled",
  "message": "Command cancelled successfully"
}
```

**Example:**
```bash
curl -X DELETE "http://localhost:8000/cancel_command/uuid-here"
```

## Data Models

### ReadFileArgs
```json
{
  "path": "string"
}
```

### RunShellArgs
```json
{
  "command": "string"
}
```

### Command Preview
```json
{
  "program": "string",
  "arguments": ["string"],
  "working_directory": "string",
  "risk_level": "low|medium|high",
  "estimated_risk": "low|medium|high"
}
```

### Command Status
- `pending`: Command previewed, awaiting confirmation
- `confirmed`: Command confirmed, ready for execution
- `completed`: Command executed successfully
- `failed`: Command execution failed
- `cancelled`: Command cancelled by user
- `expired`: Command timed out

## Risk Assessment

Commands are automatically categorized by risk level:

### Low Risk
- `ls`, `du`, `git`, `docker`, `kubectl`
- Read-only operations
- Safe system queries

### Medium Risk
- `rm`, `cp`, `mv`, `mkdir`, `touch`
- File modifications
- Non-destructive operations

### High Risk
- Unknown programs
- Complex operations
- Potentially destructive commands

## Error Handling

### HTTP Status Codes
- `200 OK`: Success
- `400 Bad Request`: Invalid input
- `403 Forbidden`: Access denied
- `404 Not Found`: Resource not found
- `410 Gone`: Resource expired
- `415 Unsupported Media Type`: Invalid file format
- `500 Internal Server Error`: Server error
- `504 Gateway Timeout`: Command timeout

### Error Response Format
```json
{
  "detail": "Error description"
}
```

## Rate Limiting

Currently, no rate limiting is implemented. For production use, consider implementing rate limiting to prevent abuse.

## Security Features

### Command Validation
- Dangerous pattern blocking
- Shell metacharacter filtering
- Command allowlisting
- Working directory restrictions

### File Access Security
- Path traversal protection
- Base directory restrictions
- UTF-8 encoding enforcement

### Timeout Protection
- Configurable command timeouts
- Process cleanup on timeout

## Examples

### Complete Workflow Example

1. **Preview Command**
```bash
curl -X POST "http://localhost:8000/run_shell_preview" \
  -H "Content-Type: application/json" \
  -d '{"command": "rm -rf /tmp/test_files"}'
```

2. **Confirm Command**
```bash
curl -X POST "http://localhost:8000/run_shell_confirmed/command-uuid" \
  -H "Content-Type: application/json" \
  -d '{"confirmed": true}'
```

3. **Check Status**
```bash
curl "http://localhost:8000/command_status/command-uuid"
```

### File Reading Example
```bash
curl -X POST "http://localhost:8000/read_file" \
  -H "Content-Type: application/json" \
  -d '{"path": "config.json"}'
```

### Interactive Command Execution
```bash
# First, preview the command
curl -X POST "http://localhost:8000/run_shell_interactive" \
  -H "Content-Type: application/json" \
  -d '{"command": "git status"}'

# Then execute the confirmed command using the returned command_id
curl -X POST "http://localhost:8000/run_shell_confirmed/your-command-id" \
  -H "Content-Type: application/json" \
  -d '{"confirmed": true}'
```

## Integration Examples

### Open WebUI Integration
```javascript
// Example Open WebUI tool configuration
{
  "name": "run_shell_with_confirmation",
  "description": "Execute shell commands with user confirmation",
  "parameters": {
    "type": "object",
    "properties": {
      "command": {
        "type": "string",
        "description": "Shell command to execute"
      }
    },
    "required": ["command"]
  }
}
```

### Python Client Example
```python
import requests

def run_command_with_confirmation(command):
    # Preview command
    preview = requests.post(
        "http://localhost:8000/run_shell_preview",
        json={"command": command}
    ).json()
    
    command_id = preview["command_id"]
    
    # Confirm and execute
    result = requests.post(
        f"http://localhost:8000/run_shell_confirmed/{command_id}",
        json={"confirmed": True}
    ).json()
    
    return result
```

## Testing

### Health Check
```bash
curl "http://localhost:8000/docs"  # OpenAPI documentation
```

### Command Validation Test
```bash
# Test the interactive endpoint - this will return confirmation required
curl -X POST "http://localhost:8000/run_shell_interactive" \
  -H "Content-Type: application/json" \
  -d '{"command": "rm -rf /tmp/test"}'
```

## Support

For issues and questions:
1. Check the [SETUP.md](SETUP.md) for configuration help
2. Review [ARCHITECTURE.md](ARCHITECTURE.md) for design decisions
3. Check server logs for detailed error information
4. Verify environment variable configuration
