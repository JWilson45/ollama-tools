import pathlib

def read_file(path: str) -> str:
    """
    Reads a file from the current working directory.
    """
    base_path = pathlib.Path.cwd()
    file_path = base_path / path
    try:
        file_path = file_path.resolve()
        if not str(file_path).startswith(str(base_path)):
            return "Error: Access not allowed."
        with open(file_path, "r", encoding="utf-8") as f:
            return f.read()
    except Exception as e:
        return f"Error reading file: {e}"