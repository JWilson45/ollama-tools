import os
from pathlib import Path


# Base directory configuration
BASE = Path(os.getenv("BASE_DIR", ".")).resolve()

# Server configuration
TOOLS_HOST = os.getenv("TOOLS_HOST", "127.0.0.1")
TOOLS_PORT = int(os.getenv("TOOLS_PORT", "8000"))
