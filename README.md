## Simple project to play around with netmiko, nornir and Cisco CBS220 switch

### Setup
`pip install -r requirements.txt`


### Basic usage
`python main.py <mode(file/switch)> <port_number(1-10)>`

examples:

`python main.py file 1`
`python main.py switch 1`

Nornir (online only, needs config):
`python nornir_runner.py`

### TESTING:

`pytest tests/`

`robot --pythonpath . robot/tests/port_status.robot`

### OFFLINE only:

`pytest tests/ -m offline`

`robot --pythonpath . --include offline robot/tests/port_status.robot`