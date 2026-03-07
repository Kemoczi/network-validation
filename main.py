from validators.basic import check_port_info

def main(port) -> None:
    try:
        port_info = check_port_info(port)
        if port_info["Status"] == "connected":
            print(f"Port gi{port} is open.")
        elif port_info["Status"] == "notconnect":
            print(f"Port gi{port} is closed.")
        else:
            print(f"Port gi{port} status is unknown.")

        print(
            f"Port details:\n"
            f"VLAN: {port_info['Vlan']}\n"
            f"Duplex: {port_info['Duplex']}\n"
            f"Speed: {port_info['Speed']}\n"
            f"Type: {port_info['Type']}\n"
        )
    except ValueError as exc:
        print("Error: ", exc)

if __name__ == "__main__":
    main("dddd")