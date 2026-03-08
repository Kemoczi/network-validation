from validators.basic import get_port_info
import sys

def main(port) -> None:
    try:
        port_num = int(port)
        if not (1 <= port_num <= 10) or len(str(port)) > 2 or str(port).startswith("0"):
            raise ValueError(f"Port number must be integer 1-10, got: {port}.")
        else:
            port_info = get_port_info(port_num)
    except ValueError as exc:
        raise exc

    print(
        f"Port gi{port} details:\n"
        f"Status: {port_info['Status']}\n"
        f"Name: {port_info['Name']}\n"
        f"VLAN: {port_info['Vlan']}\n"
        f"Duplex: {port_info['Duplex']}\n"
        f"Speed: {port_info['Speed']}\n"
        f"Type: {port_info['Type']}\n"
    )

if __name__ == "__main__":
    try:
        port = sys.argv[1]
        main(port)
    except IndexError:
        print("Error: You must provide a port number")
    except ValueError as exc:
        print(exc)
