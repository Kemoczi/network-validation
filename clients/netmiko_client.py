import os
from dotenv import load_dotenv
from netmiko import ConnectHandler
from errors import ResponseReadError
from netmiko.exceptions import ReadTimeout


def get_switch_config():
    load_dotenv()
    required_vars = [
        "SWITCH_HOST",
        "SWITCH_USERNAME",
        "SWITCH_PASSWORD"
    ]

    missing = [name for name in required_vars if not os.getenv(name)]
    if missing:
        raise ResponseReadError(
            f"Missing required environment variables: {', '.join(missing)}"
        )
    return {
        "host": os.getenv("SWITCH_HOST"),
        "username": os.getenv("SWITCH_USERNAME"),
        "password": os.getenv("SWITCH_PASSWORD")
    }

switch_config = get_switch_config()

SWITCH_CONFIG = {
    "device_type": "cisco_s200",
    **switch_config,
}


def get_response(cmd:str) -> str:
    connection = None
    try:
        connection = ConnectHandler(**SWITCH_CONFIG)
        return connection.send_command(cmd)
    except ReadTimeout as exc:
        raise ResponseReadError(f"Timed out while reading response for command: {cmd}") from exc
    finally:
        if connection is not None:
            connection.disconnect()
