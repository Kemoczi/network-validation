from validators.basic import get_port_info
from clients import file_client, netmiko_client

# __all__ = ["get_port_status"] Not needed here - there's only one function

def get_port_status(port: int, mode: str) -> str:
    if mode == "file":
        response = file_client.get_response("show interfaces status gi1-10")
    elif mode == "switch":
        response = netmiko_client.get_response("show interfaces status gi1-10")
    else:
        response = None

    port_info = get_port_info(port, response)

    return port_info["Status"]
