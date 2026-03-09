import pytest
from validators import basic as validator
from clients import netmiko_client, file_client
from errors import PortNotFoundError

COMMAND = "show interfaces status gi1-10"

@pytest.fixture(scope="module")
def file_response():
    return file_client.get_response(COMMAND)

@pytest.fixture(scope="module")
def switch_response():
    return netmiko_client.get_response(COMMAND)

PORT_DATA = [
    (1, "connected"),
    (2, "connected"),
    (3, "connected"),
    (4, "connected"),
    (5, "connected"),
    (6, "notconnect"),
    (7, "notconnect"),
    (8, "notconnect"),
    (9, "notconnect"),
    (10, "notconnect")
]


@pytest.mark.parametrize('port, status', PORT_DATA)
def test_status_offline(port, file_response, status):
    assert validator.get_port_info(port, file_response)["Status"] == status


@pytest.mark.parametrize('port, status', PORT_DATA)
def test_status_online(port, switch_response, status):
    assert validator.get_port_info(port, switch_response)["Status"] == status


@pytest.mark.parametrize('port', [11, 12, 13])
def test_wrong_port_offline(port, file_response):
    with pytest.raises(PortNotFoundError, match="not found"):
        validator.get_port_info(port, file_response)

def test_wrong_command_online():
    assert netmiko_client.get_response("bad command") == "Unknown command"
