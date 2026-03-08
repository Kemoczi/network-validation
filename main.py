from validators.basic import check_port_info
import sys

def main(port) -> None:
    try:
        port_info = check_port_info(port)

        print(
            f"Port gi{port} details:\n"
            f"Status: {port_info['Status']}\n"
            f"Name: {port_info['Name']}\n"
            f"VLAN: {port_info['Vlan']}\n"
            f"Duplex: {port_info['Duplex']}\n"
            f"Speed: {port_info['Speed']}\n"
            f"Type: {port_info['Type']}\n"
        )
    except TypeError as exc:
        print("Error: ", exc)

if __name__ == "__main__":
    try:
        main(sys.argv[1])
    except IndexError:
        print("Error: You must provide a port number")
    except ValueError as exc:
        print("Error: ", exc)