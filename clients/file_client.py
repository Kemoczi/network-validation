from pathlib import Path


def get_file_response(cmd: str) -> str:
    filename = str.lower(cmd).replace(" ", "_")
    if cmd == "show interfaces status gi1-10":
        file = Path(f"sample_outputs/{filename}.txt")
        with file.open(encoding='utf-8') as f:
            return f.read()
    else:
        raise ValueError(f"Unknown command: {cmd}")