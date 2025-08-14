from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import uvicorn

# Import tools from the tools package
from tools.file_operations import read_file, ReadFileArgs
from tools.config import BASE, TOOLS_HOST, TOOLS_PORT

# FastAPI app that exposes tools via OpenAPI so Open WebUI can call them
app = FastAPI(
    title="Local Tools",
    description="OpenAPI tool server for Open WebUI",
    version="1.0.0",
)

# Allow calls from the Open WebUI frontend in your browser (localhost)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://127.0.0.1:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/read_file", operation_id="read_file")
def read_file_endpoint(args: ReadFileArgs):
    """
    Read a UTF-8 text file relative to BASE (current working directory by default).
    Returns {"content": "..."} or an error.
    """
    return read_file(args, BASE)


def main():
    # Allow overriding host/port with env vars if desired
    uvicorn.run("main:app", host=TOOLS_HOST, port=TOOLS_PORT, reload=False)


if __name__ == "__main__":
    main()
