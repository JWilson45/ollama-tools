from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from pathlib import Path
import uvicorn
import os

# FastAPI app that exposes tools via OpenAPI so Open WebUI can call them
app = FastAPI(
    title="Local Tools",
    description="OpenAPI tool server for Open WebUI",
    version="1.0.0",
)

# Allow calls from the Open WebUI frontend in your browser (localhost)
# You can add more origins if needed.
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://127.0.0.1:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Restrict file access to the directory where the server is launched,
# or override with the BASE_DIR environment variable if you want.
BASE = Path(os.getenv("BASE_DIR", ".")).resolve()

class ReadFileArgs(BaseModel):
    path: str

@app.post("/read_file", operation_id="read_file")
def read_file(args: ReadFileArgs):
    """
    Read a UTF-8 text file relative to BASE (current working directory by default).
    Returns {"content": "..."} or an error.
    """
    fp = (BASE / args.path).resolve()
    if not str(fp).startswith(str(BASE)):
        raise HTTPException(status_code=403, detail="Access outside base directory is not allowed.")
    try:
        text = fp.read_text(encoding="utf-8")
        return {"content": text}
    except FileNotFoundError:
        raise HTTPException(status_code=404, detail=f"File not found: {args.path}")
    except UnicodeDecodeError:
        raise HTTPException(status_code=415, detail="Only UTF-8 text files are supported.")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error reading file: {e}")

def main():
    # Allow overriding host/port with env vars if desired
    host = os.getenv("TOOLS_HOST", "0.0.0.0")
    port = int(os.getenv("TOOLS_PORT", "8000"))
    uvicorn.run("main:app", host=host, port=port, reload=False)

if __name__ == "__main__":
    main()
