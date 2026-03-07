from clients.file_client import get_file_response


def get_resp_lines(response: str) -> list[str]:
    lines_table = []
    lines = response.splitlines()
    for line in lines:
        if line == "":
            break
        column_items = line.split()
        lines_table.append(column_items)
    return lines_table


def get_port_line(port: str, resp_lines: list[str]) -> str:
    for line in resp_lines:
        if line[0] == port:
            return line
    return "Port not found"


def parse_port_line(resp_lines: list[str]) -> dict[str, int]:
    port_index = resp_lines[0].index("Port")
    # name_index = resp_lines[0].index("Name")
    # TODO: figure out what about names, now subtracting -1 from index
    status_index = resp_lines[0].index("Status") - 1
    vlan_index = resp_lines[0].index("Vlan") - 1
    duplex_index = resp_lines[0].index("Duplex") - 1
    speed_index = resp_lines[0].index("Speed") - 1
    type_index = resp_lines[0].index("Type") - 1
    columns = {"Port": port_index, "Status": status_index, "Vlan": vlan_index, "Duplex": duplex_index, "Speed": speed_index, "Type": type_index}

    return columns


def get_port_info(port: int) -> dict[str, str]:
    port_name = f"gi{port}"
    response = get_file_response("show interfaces status gi1-10")
    resp_lines = get_resp_lines(response)
    port_line = get_port_line(port_name, resp_lines)
    fields = parse_port_line(resp_lines)

    info = {
        "Port": port_line[fields["Port"]],
        "Status": port_line[fields["Status"]],
        "Vlan": port_line[fields["Vlan"]],
        "Duplex": port_line[fields["Duplex"]],
        "Speed": port_line[fields["Speed"]],
        "Type": port_line[fields["Type"]]
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
