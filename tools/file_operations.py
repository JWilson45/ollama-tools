from fastapi import HTTPException
from pydantic import BaseModel
from pathlib import Path


class ReadFileArgs(BaseModel):
    path: str


def read_file(args: ReadFileArgs, base_dir: Path):
    """
    Read a UTF-8 text file relative to BASE (current working directory by default).
    Returns {"content": "..."} or an error.
    """
    fp = (base_dir / args.path).resolve()
    if not str(fp).startswith(str(base_dir)):
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
