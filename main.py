import sys

from errors import InvalidPortError, NetworkValidationError, InvalidModeError
from validators.basic import get_port_info
from clients import file_client, netmiko_client


def parse_port_arg(port_raw: str) -> int:
    try:
        port_num = int(port_raw)
    except ValueError as exc:
        raise InvalidPortError(
            f"Port number must be an integer from 1 to 10, got: {port_raw}"
        ) from exc

    if not 1 <= port_num <= 10:
        raise InvalidPortError(
            f"Port number must be in range 1-10, got: {port_raw}"
        )

    if port_raw.startswith("0"):
        raise InvalidPortError(
            f"Port number must not start with 0, got: {port_raw}"
        )

    return port_num

COMMAND = "show interfaces status gi1-10"
def main(mode: str, port_raw: str) -> None:
    port_num = parse_port_arg(port_raw)
    mode = mode.lower().strip()

    if mode == "file":
        response = file_client.get_response(COMMAND)
    elif mode == "switch":
        response = netmiko_client.get_response(COMMAND)
    else:
        raise InvalidModeError(f"Invalid mode: {mode}. Use 'file' or 'switch'")
    port_info = get_port_info(port_num, response)

    print(
        f"Port gi{port_raw} details:\n"
        f"Status: {port_info['Status']}\n"
        f"Name: {port_info['Name']}\n"
        f"VLAN: {port_info['Vlan']}\n"
        f"Duplex: {port_info['Duplex']}\n"
        f"Speed: {port_info['Speed']}\n"
        f"Type: {port_info['Type']}\n"
    )

if __name__ == "__main__":
    try:
        mode_arg = sys.argv[1]
        port_arg = sys.argv[2]
    except IndexError:
        print("Error: You must provide a mode (file/switch) and port number")
        raise SystemExit(1)

    try:
        main(mode_arg, port_arg)
    except NetworkValidationError as exc:
        print(f"Error: {exc}")
        raise SystemExit(1)
