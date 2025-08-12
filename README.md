

# Ollama Tools — Local Tool Server for Open WebUI

This project provides a local **OpenAPI-compatible tool server** that you can connect to [Open WebUI](https://github.com/open-webui/open-webui) to extend your Ollama models with custom capabilities such as **file reading**.

## Overview

We use:
- **FastAPI** to define and serve tools as HTTP endpoints
- **Poetry** for dependency management
- **Open WebUI** in Docker, connected to your **host's Ollama** (not containerized Ollama) for maximum performance on macOS (Metal acceleration works natively)
- `host.docker.internal` to bridge between the Docker container and your Mac

## Prerequisites

- **macOS** with Homebrew installed
- [Ollama](https://ollama.com) running natively on your Mac
- [Docker Desktop](https://www.docker.com/products/docker-desktop/)
- [Poetry](https://python-poetry.org/docs/#installation) installed via Homebrew:
  ```bash
  brew install poetry
  ```
- [Open WebUI](https://github.com/open-webui/open-webui) running via Docker Compose (this repo includes a config)

## Installation

1. **Clone this repo**
   ```bash
   git clone https://github.com/jwilson45/ollama-tools.git
   cd ollama-tools
   ```

2. **Install dependencies**
   ```bash
   poetry install --no-root
   ```

3. **Run the tool server**
   ```bash
   poetry run python main.py
   ```
   or directly with uvicorn:
   ```bash
   poetry run uvicorn tool_server:app --host 0.0.0.0 --port 8000
   ```

## How the Tool Server Works

- We expose `/read_file` as a POST endpoint with this signature:
  ```json
  {
    "path": "relative/or/absolute/path/to/file.txt"
  }
  ```
- The tool server only allows access to files **within the base directory** where the server was started (sandboxed).
- The OpenAPI spec is automatically available at:
  ```
  http://localhost:8000/openapi.json
  ```

## Connecting to Open WebUI

1. In your **docker-compose.yml** for Open WebUI, ensure `OLLAMA_BASE_URL` points to your host's Ollama:
   ```yaml
   environment:
     - OLLAMA_BASE_URL=http://host.docker.internal:11434
   ```

2. Start or restart Open WebUI:
   ```bash
   docker compose up -d
   ```

3. In Open WebUI:
   - Go to **Settings → Tools → Manage Tool Servers**
   - Click **Add Server**
   - Enter:
     ```
     http://host.docker.internal:8000/openapi.json
     ```
   - Save.

4. Start a new chat, enable **Tools**, and select your Ollama model (e.g., `qwen3:4b`).

## Example Usage in Chat

```
Read notes.txt and summarize it.
```

The model will call `read_file` via the tool server, receive the file content, and then use it to respond.

## Changing the Base Directory

By default, the tool server reads from the directory you start it in. To change this, set the `BASE_DIR` environment variable:

```bash
BASE_DIR=/path/to/files poetry run python tool_server.py
```

## Development Notes

- You can add more tools by defining additional FastAPI endpoints.
- All endpoints should be OpenAPI-compatible for Open WebUI to discover them.
- To quickly reload changes during development:
  ```bash
  poetry run uvicorn tool_server:app --reload --host 0.0.0.0 --port 8000
  ```

## License

MIT License