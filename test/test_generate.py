from quartus import Setup


def test_devices_setup():
    _setup = Setup()
    family = _setup.lookup_device(device='EP4CE22F17C6')
    assert family == 'Cyclone IV E'.upper()