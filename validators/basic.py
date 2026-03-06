

def check_port_state(port: int, response: str) -> str:
    if 1 <= port <= 10:
        port_line = response.splitlines()[port]
        if port_line.find("connected") != -1:
            return "connected"
        else:
            return "not connected"
    else:
        raise ValueError("Port must be between 1 and 10")
