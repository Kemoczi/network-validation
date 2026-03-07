from clients.file_client import get_file_response


def get_resp_lines(response: str) -> list[str]:
    lines_table = []
    lines = response.splitlines()
    for line in lines:
        if line == "":
            break
        lines_table.append(line)
    return lines_table


def get_port_line(port: str, resp_lines: list[str]) -> str:
    for line in resp_lines:
        if line.startswith(port):
            return line
    return "Port not found"


def parse_port_line(resp_lines: list[str]) -> dict[str, int]:
    header = resp_lines[0]
    port_index = header.find("Port")
    name_index = header.find("Name")
    status_index = header.find("Status")
    vlan_index = header.find("Vlan")
    duplex_index = header.find("Duplex")
    speed_index = header.find("Speed")
    type_index = header.find("Type")

    columns = {
        "Port": port_index,
        "Name": name_index,
        "Status": status_index,
        "Vlan": vlan_index,
        "Duplex": duplex_index,
        "Speed": speed_index,
        "Type": type_index
    }

    return columns


def get_port_info(port: int) -> dict[str, str]:
    port_name = f"gi{port}"
    response = get_file_response("show interfaces status gi1-10")
    resp_lines = get_resp_lines(response)
    port_line = get_port_line(port_name, resp_lines)
    fields = parse_port_line(resp_lines)

    info = {
        "Port": port_line[fields["Port"]:fields["Name"]].strip(),
        "Name": port_line[fields["Name"]:fields["Status"]].strip(),
        "Status": port_line[fields["Status"]:fields["Vlan"]].strip(),
        "Vlan": port_line[fields["Vlan"]:fields["Duplex"]].strip(),
        "Duplex": port_line[fields["Duplex"]:fields["Speed"]].strip(),
        "Speed": port_line[fields["Speed"]:fields["Type"]].strip(),
        "Type": port_line[fields["Type"]:len(port_line)]
    }
    return info

def check_port_info(port: int) -> dict[str, str]:
    try:
        port_num = int(port)
    except:
        raise ValueError(f"Port number must be integer, got: {port}.")
    if 1 <= port_num <= 10:
        info = get_port_info(port_num)
        return info
    else:
        raise ValueError(f"Port number must be integer 1-10, got: {port}.")
