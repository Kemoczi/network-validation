from pathlib import Path
from errors import ResponseReadError, UnknownCommandError

SUPPORTED_COMMANDS = {
    "show interfaces status gi1-10": "show_interfaces_status_gi1-10.txt",
}

PROJECT_ROOT = Path(__file__).resolve().parent.parent
SAMPLE_OUTPUTS_DIR = PROJECT_ROOT / "sample_outputs"

def get_response(cmd: str) -> str:
    filename = SUPPORTED_COMMANDS.get(cmd)
    if filename is None:
        raise UnknownCommandError(f"Unsupported command: {cmd}")

    file_path = SAMPLE_OUTPUTS_DIR / filename

    try:
        with file_path.open(encoding="utf-8") as file:
            return file.read()
    except FileNotFoundError as exc:
        raise ResponseReadError(
            f"Sample output file not found for command '{cmd}': {file_path}"
        ) from exc
    except OSError as exc:
        raise ResponseReadError(
            f"Could not read sample output file for command '{cmd}': {file_path}"
        ) from exc
