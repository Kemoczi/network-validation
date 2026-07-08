import time
from typing import Any

from snmp import Engine, SNMPv2c

engine = Engine(SNMPv2c)

switch = engine.Manager("192.168.0.12", community=b"monitoring")


def countdown(t: int) -> None:
    while t:
        print(f"\r{t}", end='', flush=True)
        time.sleep(1)
        t -= 1
    print("\r", end='', flush=True)


def get_traffic(if_count: int)-> tuple[list[Any], list[Any]]:
    snmp_oct_in_oid = "1.3.6.1.2.1.31.1.1.1.6."
    snmp_oct_out_oid = "1.3.6.1.2.1.31.1.1.1.10."

    kb_in_start = [switch.get(snmp_oct_in_oid + str(port))[0].value.value / 1_000 for port in range(1, if_count + 1)]
    kb_out_start = [switch.get(snmp_oct_out_oid + str(port))[0].value.value / 1_000 for port in range(1, if_count + 1)]

    countdown(1)

    kb_in_end = [switch.get(snmp_oct_in_oid + str(port))[0].value.value / 1_000 for port in
                   range(1, if_count + 1)]
    kb_out_end = [switch.get(snmp_oct_out_oid + str(port))[0].value.value / 1_000 for port in
                    range(1, if_count + 1)]

    delta_in = [kb_in_end[i] - kb_in_start[i] for i in range(if_count)]
    delta_out = [kb_out_end[i] - kb_out_start[i] for i in range(if_count)]

    return delta_in, delta_out


def get_if_count() -> int:
    all_ifs = switch.get("1.3.6.1.2.1.2.1.0")[0].value.value
    if_count = 0

    for i in range(1, all_ifs):
        if_type = switch.get(f"1.3.6.1.2.1.2.2.1.3.{i}")
        try:
            _ = if_type[0].value.value
            if_count += 1
        except AttributeError:
            continue
    return if_count


def get_alias(if_count: int) -> list[str]:
    aliases = []

    for port in range(1, if_count + 1):
        alias = switch.get(f"1.3.6.1.2.1.31.1.1.1.18.{port}")
        if alias[0].value.data != b'':
            aliases.append(alias[0].value.data.decode('utf-8'))
    # if no alias, fall back to if generic name
        else:
           aliases.append(
               switch.get(f"1.3.6.1.2.1.2.2.1.2.{port}")[0]
               .value.data.decode('utf-8')
           )

    return aliases


def get_oper_status(if_count: int) -> list[str]:
    oper_status_oid = "1.3.6.1.2.1.2.2.1.8."
    oper_status = [switch.get(oper_status_oid + str(port)) for port in range(1, if_count + 1)]

    oper_status_parsed = []

    for status in oper_status:
        match status[0].value.value:
            case 1:
                oper_status_parsed.append("UP")
            case 2:
                oper_status_parsed.append("DOWN")
            case _:
                oper_status_parsed.append("UNKNOWN")

    return oper_status_parsed


def get_errors(if_count: int) -> tuple[list[int], list[int]]:
    errors_in_oid = "1.3.6.1.2.1.2.2.1.14."
    errors_out_oid = "1.3.6.1.2.1.2.2.1.20."

    errors_in_start = [switch.get(errors_in_oid + str(port))[0].value.value for port in range(1, if_count + 1)]
    errors_out_start = [switch.get(errors_out_oid + str(port))[0].value.value for port in range(1, if_count + 1)]

    errors_in_end = [switch.get(errors_in_oid + str(port))[0].value.value for port in range(1, if_count + 1)]
    errors_out_end = [switch.get(errors_out_oid + str(port))[0].value.value for port in range(1, if_count + 1)]

    errors_in = [errors_in_end[i] - errors_in_start[i] for i in range(if_count)]
    errors_out = [errors_out_end[i] - errors_out_start[i] for i in range(if_count)]

    return errors_in, errors_out


def get_speed(if_count: int) -> list[int]:
    speed_oid = "1.3.6.1.2.1.31.1.1.1.15."
    speeds = [switch.get(speed_oid + str(port))[0].value.value for port in range(1, if_count + 1)]

    return speeds


def create_table(rows: list[dict]) -> str:
    headers = ["Port", "Name", "Status", "Max speed [Mbps]", "In Errors", "Out Errors", "kB in", "kB out"]

    table_rows = []
    for row in rows:
        table_rows.append([
            str(row["port"]),
            str(row["name"]),
            str(row["status"]),
            str(row["speed"]),
            str(row["errors_in"]),
            str(row["errors_out"]),
            str(row["kb_in"]),
            str(row["kb_out"]),
        ])

    widths = []
    for i, header in enumerate(headers):
        max_width = len(header)
        for row in table_rows:
            max_width = max(max_width, len(row[i]))
        widths.append(max_width)

    def format_row(values: list[str]) -> str:
        return " | ".join(
            value.ljust(width) for value, width in zip(values, widths)
        )

    separator = "-+-".join("-" * width for width in widths)

    lines = [
        format_row(headers),
        separator,
    ]

    for row in table_rows:
        lines.append(format_row(row))

    return "\n".join(lines)


def get_snapshot(if_count: int) -> str:
    rows = []
    names = get_alias(if_count)
    statuses = get_oper_status(if_count)
    speeds = get_speed(if_count)
    errors_in, errors_out = get_errors(if_count)
    kb_in, kb_out = get_traffic(if_count)

    for if_idx in range(0, if_count):
        rows.append(
            {
                "port": if_idx + 1,
                "name": names[if_idx],
                "status": statuses[if_idx],
                "speed": speeds[if_idx],
                "errors_in": errors_in[if_idx],
                "errors_out": errors_out[if_idx],
                "kb_in": f"{kb_in[if_idx]:.2f}",
                "kb_out": f"{kb_out[if_idx]:.2f}"
            }
        )

    return create_table(rows)


if __name__ == "__main__":

    print(
        get_snapshot(get_if_count())
        )
