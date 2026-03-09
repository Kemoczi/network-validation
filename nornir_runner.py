from dotenv import load_dotenv
from nornir import InitNornir
from nornir_netmiko.tasks import netmiko_send_command
from validators.basic import get_port_info

load_dotenv()

nr = InitNornir(config_file="config.yaml")

nr = nr.filter(site="Olesnica", role="switch")

def get_output(task):
    task.run(task=netmiko_send_command, command_string="show version")
    task.run(task=netmiko_send_command, command_string="show interfaces status gi1-10")

results = nr.run(task=get_output)
# result = nr.run(task=netmiko_send_command, command_string="show version")

version = results['CBS220'][1].result
cmd_output = results['CBS220'][2].result

# if no filter
# example = results['ExampleDevice'][1].result
# print(example)

print(version)

port_num = 1
port_info = get_port_info(port_num, cmd_output)

print(
    f"\n"
    f"PORT GI{port_num} DETAILS:\n"
    f"Status: {port_info['Status']}\n"
    f"Name: {port_info['Name']}\n"
    f"VLAN: {port_info['Vlan']}\n"
    f"Duplex: {port_info['Duplex']}\n"
    f"Speed: {port_info['Speed']}\n"
    f"Type: {port_info['Type']}\n"
)
