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
    snmp_oct_in = f"1.3.6.1.2.1.31.1.1.1.6.{port}"
    snmp_oct_out = f"1.3.6.1.2.1.31.1.1.1.10.{port}"

    start_in = switch.get(snmp_oct_in)[0].value.value
    start_out = switch.get(snmp_oct_out)[0].value.value

    print(f"\nGathering traffic on port {port} for {t} seconds, please wait...\n")
    countdown(t)

    end_in = switch.get(snmp_oct_in)[0].value.value
    end_out = switch.get(snmp_oct_out)[0].value.value

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


def get_alias(port: int) -> str:
    alias = switch.get(f"1.3.6.1.2.1.31.1.1.1.18.{port}")
    if alias[0].value.data != b'':
        return alias[0].value.data.decode('utf-8')
    # if no alias, fall back to if generic name
    else:
        return switch.get(f"1.3.6.1.2.1.2.2.1.2.{port}")[0].value.data.decode('utf-8')


def get_oper_status(port: int) -> str:
    oper_status = switch.get(f"1.3.6.1.2.1.2.2.1.8.{port}")

    if (oper_status[0].value.value == 1):
        return "UP"
    else:
        return "DOWN"


def get_snapshot() -> list[dict]:
    rows = []
    row = {"Name": ''}
    if_count = get_if_count()

    for i in range(1, if_count + 1):
        print(get_alias(i), get_oper_status(i))


if __name__ == "__main__":
    PORT = 5
    TIME_S = 20

    get_snapshot()

    # data = count_traffic(PORT, TIME_S)
    #
    # print(f"MB In: {data[0]}")
    # print(f"MB Out: {data[1]}")
