# Ollama Tools - Architecture & Decision Log

## Project Overview
A FastAPI-based tool server that provides secure shell command execution and file operations for AI agents, with interactive confirmation workflows.

## Key Architectural Decisions

### 1. Tool Server Architecture
**Decision**: Modular tool package structure with centralized configuration
**Rationale**: 
- Separation of concerns for maintainability
- Easy to add new tools without modifying main server
- Centralized configuration management
- Clean imports and package structure

**Alternatives Considered**:
- Monolithic single file (rejected: harder to maintain)
- Plugin-based architecture (rejected: overkill for current scope)

**Date**: 2024-01-15
**Status**: Implemented

### 2. Security Model
**Decision**: Multi-layered command validation with allowlisting
**Rationale**:
- Prevents dangerous command execution
- Configurable security policies
- Blocks shell metacharacters for safety
- Environment variable configuration for flexibility

**Security Layers**:
1. Always-blocked dangerous patterns
2. Configurable command allowlist
3. Shell metacharacter blocking
4. Working directory restrictions
5. Command timeout limits

**Date**: 2024-01-15
**Status**: Implemented

### 3. Interactive Confirmation Workflow
**Decision**: Two-step preview and confirmation process
**Rationale**:
- Gives users control over command execution
- Prevents accidental execution of dangerous commands
- Provides risk assessment before execution
- Maintains audit trail of all commands
- **Eliminates immediate execution bypass** for maximum security

**Workflow**:
1. Command preview with validation
2. Risk assessment and user review
3. Explicit confirmation required
4. Execution with result tracking

**Security Features**:
- **No immediate execution**: All commands require confirmation
- **Mandatory user review**: AI agents cannot bypass confirmation
- **Complete audit trail**: Every command request is tracked

**Date**: 2024-01-15
**Status**: Implemented

## File Structure & Dependencies

```
ollama-tools/
├── main.py                 # FastAPI server entry point
├── tools/
│   ├── __init__.py        # Package initialization and exports
│   ├── config.py          # Centralized configuration
│   ├── file_operations.py # File reading operations
│   └── shell.py          # Shell command execution
├── ARCHITECTURE.md        # This decision log
├── SETUP.md              # Environment and setup guide
└── API_REFERENCE.md      # API endpoint documentation
```

## Configuration Management

### Environment Variables
- `BASE_DIR`: Working directory for file operations
- `TOOLS_HOST`: Server host binding
- `TOOLS_PORT`: Server port
- `ALLOW_CMDS`: Comma-separated list of allowed commands
- `TOOLS_TIMEOUT`: Command execution timeout
- `BLOCK_CMDS`: Additional blocked command patterns

### Configuration Philosophy
- **Security by default**: Restrictive policies unless explicitly allowed
- **Environment-based**: Configuration via environment variables
- **Runtime validation**: All commands validated before execution

## API Design Decisions

### 1. RESTful Endpoints
**Decision**: Standard REST API with clear resource naming
**Rationale**: Familiar to developers, easy to integrate with existing tools

### 2. Error Handling
**Decision**: HTTP status codes with descriptive error messages
**Rationale**: Standard web practices, easy debugging and integration

### 3. Response Format
**Decision**: Consistent JSON responses with status and data
**Rationale**: Predictable structure for AI agents and frontends

## Security Considerations

### Command Execution Safety
- **No shell interpretation**: Commands run directly via subprocess
- **Working directory isolation**: Restricted to BASE_DIR
- **Command timeout**: Prevents hanging processes
- **Input validation**: All commands validated before execution
- **Mandatory confirmation**: No immediate execution bypass possible

### Security Model Evolution
**Previous Model**: Had both immediate execution and confirmation endpoints
**Current Model**: Only confirmation-based execution for maximum security

**Security Improvements**:
- **Removed `/run_shell` endpoint**: Eliminates immediate execution risk
- **Mandatory confirmation workflow**: All commands require user approval
- **AI agent safety**: No way for AI to execute commands without user consent

### File Access Security
- **Path traversal protection**: Prevents access outside BASE_DIR
- **UTF-8 encoding only**: Prevents encoding-based attacks
- **Error message sanitization**: No internal path exposure

## Testing Strategy

### Unit Testing
- Individual tool functions
- Configuration validation
- Security rule enforcement

### Integration Testing
- API endpoint behavior
- End-to-end workflows
- Error handling scenarios

### Security Testing
- Command injection attempts
- Path traversal attempts
- Timeout handling

## Deployment Considerations

### Production Readiness
- **Logging**: Structured logging for audit trails
- **Monitoring**: Health checks and metrics
- **Rate limiting**: Prevent abuse
- **Authentication**: Consider adding auth for production use

### Container Deployment
- **Docker support**: Already configured
- **Environment isolation**: Proper configuration management
- **Health checks**: Container health monitoring

## Future Enhancements

### Planned Features
1. **Command history**: Persistent storage of executed commands
2. **User management**: Multi-user support with permissions
3. **Advanced workflows**: Command chaining and batch operations
4. **Plugin system**: Extensible tool architecture

### Technical Debt
1. **Database integration**: For persistent command history
2. **Authentication system**: For production deployments
3. **Rate limiting**: To prevent abuse
4. **Metrics collection**: For monitoring and optimization

## Maintenance Notes

### Regular Tasks
- Review security policies monthly
- Update blocked command patterns as needed
- Monitor command execution logs
- Review and update documentation

### Troubleshooting
- Check environment variable configuration
- Verify file permissions for BASE_DIR
- Review command allowlist settings
- Check timeout configurations

## Contributing Guidelines

### Code Standards
- Follow existing module structure
- Add comprehensive error handling
- Include security validation
- Update this document for new decisions

### Security Review
- All new tools require security review
- Command execution tools need extra scrutiny
- File access tools must respect BASE_DIR restrictions
