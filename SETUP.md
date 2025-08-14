# Setup Guide

## Prerequisites
- Python 3.13+
- Poetry for dependency management
- Git (for version control)

## Installation

### 1. Clone the Repository
```bash
git clone <your-repo-url>
cd ollama-tools
```

### 2. Install Dependencies
```bash
poetry install
```

### 3. Verify Installation
```bash
poetry run python -c "from tools import read_file, run_shell; print('Installation successful!')"
```

## Configuration

### Environment Variables

The tool server can be configured using environment variables. Create a `.env` file in your project root:

```bash
# Base directory for file operations (default: current directory)
export BASE_DIR="/path/to/your/project"

# Server configuration
export TOOLS_HOST="0.0.0.0"
export TOOLS_PORT="8000"

# Shell command security
export ALLOW_CMDS="ls,du,git,docker,kubectl"
export TOOLS_TIMEOUT="60"
export BLOCK_CMDS="sudo,su"
```

### Configuration Options

| Variable | Default | Description |
|----------|---------|-------------|
| `BASE_DIR` | `.` | Working directory for file operations |
| `TOOLS_HOST` | `0.0.0.0` | Server host binding |
| `TOOLS_PORT` | `8000` | Server port |
| `ALLOW_CMDS` | `""` | Comma-separated list of allowed commands |
| `TOOLS_TIMEOUT` | `60` | Command execution timeout in seconds |
| `BLOCK_CMDS` | `""` | Additional blocked command patterns |

### Security Configuration

#### Command Allowlisting
If you set `ALLOW_CMDS`, only those commands will be allowed:

```bash
# Allow only specific commands
export ALLOW_CMDS="ls,du,git,docker"

# Allow all commands (less secure)
export ALLOW_CMDS=""
```

#### Blocked Commands
Add additional commands to block:

```bash
# Block dangerous commands
export BLOCK_CMDS="sudo,su,rm -rf"
```

## Running the Server

### Development Mode
```bash
# Activate Poetry shell
poetry shell

# Run the server
python main.py
```

### Production Mode
```bash
# Run directly with Poetry
poetry run python main.py

# Or with specific configuration
BASE_DIR="/var/www" ALLOW_CMDS="ls,du" poetry run python main.py
```

### Docker (Alternative)
```bash
# Build and run with Docker Compose
docker-compose up --build
```

## Testing the Installation

### 1. Start the Server
```bash
poetry run python main.py
```

### 2. Test File Reading
```bash
curl -X POST "http://localhost:8000/read_file" \
  -H "Content-Type: application/json" \
  -d '{"path": "README.md"}'
```

### 3. Test Command Preview
```bash
curl -X POST "http://localhost:8000/run_shell_preview" \
  -H "Content-Type: application/json" \
  -d '{"command": "ls -la"}'
```

### 4. Test Command Execution
```bash
curl -X POST "http://localhost:8000/run_shell" \
  -H "Content-Type: application/json" \
  -d '{"command": "ls -la"}'
```

## Development Setup

### 1. Install Development Dependencies
```bash
poetry install --with dev
```

### 2. Run Tests
```bash
poetry run pytest
```

### 3. Code Formatting
```bash
poetry run black .
poetry run isort .
```

### 4. Linting
```bash
poetry run flake8
poetry run mypy .
```

## Troubleshooting

### Common Issues

#### Import Errors
```bash
# Make sure you're in the Poetry environment
poetry shell

# Verify imports work
python -c "from tools import *"
```

#### Permission Errors
```bash
# Check BASE_DIR permissions
ls -la $BASE_DIR

# Ensure the directory is readable
chmod 755 $BASE_DIR
```

#### Command Blocked
```bash
# Check ALLOW_CMDS setting
echo $ALLOW_CMDS

# Check BLOCK_CMDS setting
echo $BLOCK_CMDS

# Verify command isn't in blocked patterns
```

#### Port Already in Use
```bash
# Check what's using the port
lsof -i :8000

# Kill the process or change TOOLS_PORT
export TOOLS_PORT="8001"
```

### Debug Mode
Enable debug logging by setting the environment variable:

```bash
export PYTHONPATH="."
export LOG_LEVEL="DEBUG"
poetry run python main.py
```

## Production Deployment

### 1. Environment Setup
```bash
# Create production environment
export BASE_DIR="/var/www/production"
export TOOLS_HOST="127.0.0.1"
export TOOLS_PORT="8000"
export ALLOW_CMDS="ls,du,git"
export TOOLS_TIMEOUT="30"
```

### 2. Process Management
```bash
# Use systemd service
sudo systemctl enable ollama-tools
sudo systemctl start ollama-tools

# Or use supervisor
sudo supervisorctl start ollama-tools
```

### 3. Reverse Proxy
```bash
# Nginx configuration example
server {
    listen 80;
    server_name your-domain.com;
    
    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}
```

## Security Considerations

### 1. Network Security
- Bind to `127.0.0.1` in production (not `0.0.0.0`)
- Use reverse proxy with SSL termination
- Implement rate limiting

### 2. Command Security
- Always set `ALLOW_CMDS` in production
- Regularly review `BLOCK_CMDS`
- Monitor command execution logs

### 3. File Access
- Restrict `BASE_DIR` to necessary directories
- Ensure proper file permissions
- Audit file access patterns

## Monitoring and Logging

### 1. Health Checks
```bash
# Check server health
curl "http://localhost:8000/health"

# Check pending commands
curl "http://localhost:8000/pending_commands"
```

### 2. Log Analysis
```bash
# Monitor server logs
tail -f /var/log/ollama-tools.log

# Check for blocked commands
grep "Blocked dangerous command" /var/log/ollama-tools.log
```

## Next Steps

1. **Configure your environment** with appropriate security settings
2. **Test the endpoints** to ensure everything works
3. **Integrate with Open WebUI** or your preferred AI interface
4. **Set up monitoring** for production use
5. **Review security policies** regularly

For more information, see:
- [ARCHITECTURE.md](ARCHITECTURE.md) - Detailed architecture decisions
- [API_REFERENCE.md](API_REFERENCE.md) - API endpoint documentation
