import time
from snmp import Engine, SNMPv2c

engine = Engine(SNMPv2c)

switch = engine.Manager("192.168.0.12", community=b"monitoring")


def countdown(t: int) -> None:
    while t:
        print(f"\r{t}", end='', flush=True)
        time.sleep(1)
        t -= 1
    print("\r", end='', flush=True)


def count_traffic(port: int, t: int)-> tuple[int, int]:
    smtp_mb_in = f"1.3.6.1.2.1.31.1.1.1.6.{port}"
    smtp_mb_out = f"1.3.6.1.2.1.31.1.1.1.10.{port}"

    start_in = switch.get(smtp_mb_in)[0].value.value
    start_out = switch.get(smtp_mb_out)[0].value.value

    print(f"\nGathering traffic on port {port} for {t} seconds, please wait...\n")
    countdown(t)

    end_in = switch.get(smtp_mb_in)[0].value.value
    end_out = switch.get(smtp_mb_out)[0].value.value

    delta_in = end_in - start_in
    delta_out = end_out - start_out

    mb_in = delta_in / 1_000_000
    mb_out = delta_out / 1_000_000

    return mb_in, mb_out


def get_if_count() -> int:
    all_ifs = switch.get("1.3.6.1.2.1.2.1.0")[0].value.value
    if_count = 0

    for i in range(1, all_ifs):
        type = switch.get(f"1.3.6.1.2.1.2.2.1.3.{i}")
        try:
            _ = type[0].value.value
            if_count += 1
        except AttributeError:
            continue
    return if_count


def get_snapshot() -> list[dict]:

    rows = []
    row = {"Name": ''}

    for i in range(1, get_if_count() + 1):
        alias = switch.get(f"1.3.6.1.2.1.31.1.1.1.18.{i}")
        if alias[0].value.data != b'':
            print(alias[0].value.data.decode('utf-8'))
        else:
            print(switch.get(f"1.3.6.1.2.1.2.2.1.2.{i}")[0].value.data.decode('utf-8'))


if __name__ == "__main__":
    PORT = 5
    TIME_S = 20

    # get_snapshot()

    data = count_traffic(PORT, TIME_S)

    print(f"MB In: {data[0]}")
    print(f"MB Out: {data[1]}")
