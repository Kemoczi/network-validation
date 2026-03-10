## Simple project to play around with netmiko, nornir and Cisco CBS220 switch

### Setup
`pip install -r requirements.txt`


### Basic usage
`python main.py <port_number(1-10)> <mode(file/switch)>`

example:

`python main.py 1 switch`


### TESTING:

`pytest tests/`

`robot --pythonpath . robot/tests/port_status.robot`

### OFFLINE only:

`pytest tests/ -m offline`

`robot --pythonpath . --include offline robot/tests/port_status.robot`