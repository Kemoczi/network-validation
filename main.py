from clients.file_client import get_file_response
from validators.basic import check_port_state

def get_port_state(port: int) -> str | None:
    try:
        response = get_file_response("show interfaces status gi1-10")
        port = int(port)
        port_state = check_port_state(port, response)

        if port_state == "connected":
            return f"Port gi{port} is connected"
        elif port_state == "not connected":
            return f"Port gi{port} is not connected"
    except ValueError as exc:
        return f"Invalid port: {port}. {exc}"

def main() -> None:
    port = 7
    port_state = get_port_state(port)

    print(port_state)

if __name__ == "__main__":
    main()