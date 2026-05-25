from snmp import *

engine = Engine(SNMPv2c)  # or SNMPv2c

switch = engine.Manager("192.168.0.12", community=b"monitoring")

print("sysDescr:", switch.get("1.3.6.1.2.1.1.1.0"))
print("sysUpTime:", switch.get("1.3.6.1.2.1.1.3.0"))
print("ifDescr port2:", switch.get("1.3.6.1.2.1.2.2.1.2.2"))
print("ifOutOctets port2:", switch.get("1.3.6.1.2.1.2.2.1.16.2"))