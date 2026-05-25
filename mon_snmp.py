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
    start_in = switch.get(f"1.3.6.1.2.1.31.1.1.1.6.{port}")[0].value.value
    start_out = switch.get(f"1.3.6.1.2.1.31.1.1.1.10.{port}")[0].value.value

    print(f"\nGathering traffic on port {port} for {t} seconds, please wait...\n")
    countdown(t)

    end_in = switch.get(f"1.3.6.1.2.1.31.1.1.1.6.{port}")[0].value.value
    end_out = switch.get(f"1.3.6.1.2.1.31.1.1.1.10.{port}")[0].value.value

    delta_in = end_in - start_in
    delta_out = end_out - start_out

    mbps_in = delta_in * 8 / t / 1_000_000
    mbps_out = delta_out * 8 / t / 1_000_000

    return mbps_in, mbps_out


if __name__ == "__main__":
    PORT = 2
    TIME_S = 10

    data = count_traffic(PORT, TIME_S)

    print(f"In: {data[0]}")
    print(f"Out: {data[1]}")
