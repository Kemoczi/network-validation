''' Get command - if correct - return file content, else - throw exception '''
from pathlib import Path

def get_file_response(cmd):
    if cmd == "show interfaces status gi1-10":
        file = Path("sample_outputs/show_interfaces_status_gi1-10.txt")
        with file.open() as f:
            return f.read()
    elif cmd == "show interfaces status gi1-5":
        return "Not yet implemented"
    else:
        raise ValueError(f"Unknown command: {cmd}")