''' Get command - if correct - return file content, else - throw exception '''
from pathlib import Path

def parse_cmd_to_filename(cmd: str) -> str:
    parsed = str.lower(cmd).replace(" ", "_")
    return parsed

def get_file_response(cmd: str) -> str:
    if cmd == "show interfaces status gi1-10":
        filename = parse_cmd_to_filename(cmd)
        file = Path(f"sample_outputs/{filename}.txt")
        with file.open(encoding='utf-8') as f:
            return f.read()
    else:
        raise ValueError(f"Unknown command: {cmd}")