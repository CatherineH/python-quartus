from quartus.jtag import get_hardware

_Hardware = get_hardware()
print(_Hardware[0])

bloop = _Hardware[0].devices
print(bloop)