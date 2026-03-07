import pytest
from validators.basic import check_port_info

def test_offline_sample_pos():
    assert check_port_info(1)["Status"] == "connected"

def test_offline_sample_neg():
    assert check_port_info(10)["Status"] == "notconnect"

def test_offline_sample_exception():
    with pytest.raises(ValueError):
        assert check_port_info(11)["Status"]
