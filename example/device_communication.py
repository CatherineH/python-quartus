from quartus.jtag import get_hardware
usbblaster = None
test_device = None

# Find the USB Blaster
# Setup connection

for _hardware in get_hardware():
    if _hardware.name.find("USB-Blaster") >= 0:
        usbblaster = _hardware

print("Select JTAG chain connected to " + usbblaster.name)

# List all devices on the chain, and select the first device on the chain.
# Devices on the JTAG chain:
for _device in usbblaster.devices:
    if _device.name.find("@1") > 0:
        test_device = _device
print("Selected device: " + test_device.name)
test_device.open()
'''
# send a string
_string = "Hello world"
for i in range(len(_string)):
    # Send data to the Altera input FIFO buffer
    test_device.write(1, instance=0, instruction=True)
    test_device.write(_string[i], instance=0)
    # Read data in from the Altera output FIFO buffer
    # Check if there is anything to read
    test_device.write(2, instance=0, instruction=True)
    test_device.write(0, instance=0, length=4)
    tdi = test_device.read()
    if not int(tdi) == 1:
        test_device.write(0, instance=0, instruction=True)
        test_device.write(0, instance=0, length=8)
        tdi = test_device.read()
        print(chr(int(tdi, 2)))

# Close device.  Just used if communication error occurs
# Set IR back to 0, which is bypass mode
test_device.write(instance=0, instruction=3)
test_device.close()
'''

