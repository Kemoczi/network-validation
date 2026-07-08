import time
import subprocess
import sys
from typing import Any

from snmp import Engine, SNMPv2c

engine = Engine(SNMPv2c)

switch = engine.Manager("192.168.0.12", community=b"monitoring")


def countdown(t: int) -> None:
    while t:
        print(f"\rNext snapshot in: {t} seconds [Ctrl+C to exit]", end='', flush=True)
        time.sleep(1)
        t -= 1


def get_traffic(if_count: int)-> tuple[list[Any], list[Any]]:
    snmp_oct_in_oid = "1.3.6.1.2.1.31.1.1.1.6."
    snmp_oct_out_oid = "1.3.6.1.2.1.31.1.1.1.10."

    kb_in = [switch.get(snmp_oct_in_oid + str(port))[0].value.value / 1_000 for port in range(1, if_count + 1)]
    kb_out = [switch.get(snmp_oct_out_oid + str(port))[0].value.value / 1_000 for port in range(1, if_count + 1)]

    return kb_in, kb_out


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

    errors_in = [switch.get(errors_in_oid + str(port))[0].value.value for port in range(1, if_count + 1)]
    errors_out = [switch.get(errors_out_oid + str(port))[0].value.value for port in range(1, if_count + 1)]

    return errors_in, errors_out


def get_speed(if_count: int) -> list[int]:
    speed_oid = "1.3.6.1.2.1.31.1.1.1.15."
    speeds = [switch.get(speed_oid + str(port))[0].value.value for port in range(1, if_count + 1)]

    return speeds


def create_table(rows: list[dict]) -> str:
    headers = ["Port", "Name", "Status", "Max speed [Mbps]", "In Errors", "Out Errors", "kB/s in", "kB/s out"]

    table_rows = []
    for row in rows:
        table_rows.append([
            str(row["port"]),
            str(row["name"]),
            str(row["status"]),
            str(row["speed"]),
            str(row["errors_in"]),
            str(row["errors_out"]),
            str(row["kbps_in"]),
            str(row["kbps_out"]),
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
        "SNMP Monitor v.0.1 by Kemoczi\n",
        format_row(headers),
        separator,
    ]

    for row in table_rows:
        lines.append(format_row(row))

    return "\n".join(lines) + "\n"


def get_snapshot(if_count: int, interval: int) -> list[Any]:
    rows = []
    names = get_alias(if_count)
    statuses = get_oper_status(if_count)
    speeds = get_speed(if_count)

    errors_in_start, errors_out_start = get_errors(if_count)
    kb_in_start, kb_out_start = get_traffic(if_count)

    countdown(interval)

    errors_in_end, errors_out_end = get_errors(if_count)
    kb_in_end, kb_out_end = get_traffic(if_count)

    errors_in = [errors_in_end[i] - errors_in_start[i] for i in range(if_count)]
    errors_out = [errors_out_end[i] - errors_out_start[i] for i in range(if_count)]
    kb_in = [(kb_in_end[i] - kb_in_start[i]) / interval for i in range(if_count)]
    kb_out = [(kb_out_end[i] - kb_out_start[i]) / interval for i in range(if_count)]

    for if_idx in range(0, if_count):
        rows.append(
            {
                "port": if_idx + 1,
                "name": names[if_idx],
                "status": statuses[if_idx],
                "speed": speeds[if_idx],
                "errors_in": errors_in[if_idx],
                "errors_out": errors_out[if_idx],
                "kbps_in": f"{kb_in[if_idx]:.3f}",
                "kbps_out": f"{kb_out[if_idx]:.3f}"
            }
        )

    return rows

def monitor_loop(if_count:int, interval: int):

    rows = get_snapshot(if_count, interval)
    subprocess.run("cls", shell=True)
    print(create_table(rows))



if __name__ == "__main__":
    if_count = get_if_count()

    while True:
        try:
            monitor_loop(if_count, 10)
        except KeyboardInterrupt:
            print("\nMonitor stopped")
            sys.exit(0)
