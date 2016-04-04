from subprocess import Popen, PIPE


def get_hardware():
    """
    Gets a list of Hardware objects
    currently unimplemented
    tcl command: get_hardware_names
    :return: list of Hardware
    """
    output, error = Popen(["quartus_stp", "--tcl_eval", "get_hardware_names"],
                         stdout=PIPE, stderr=PIPE).communicate()
    _hardware = []
    for item in output.split("\n"):
        if len(item) > 0:
            _hardware.append(Hardware(name=item))
    return _hardware


class Device(object):
    """
    All functions relating to the devices
    """
    def __init__(self, hardware_name=None, name=None):
        self.name = name
        self.hardware_name = name

    def __str__(self):
        if self.name is None:
            return "Device does not exist"
        else:
            return self.name

    def open(self):
        """
        Currently unimplemented
        tcl command: open_device
        """
        pass

    def close(self):
        """
        Currently unimplemented
        tcl command: close_device
        """
        pass

    def lock(self):
        """
        Currently unimplemented
        tcl command: device_lock
        """
        pass

    def unlock(self):
        """
        Currently unimplemented
        tcl command: device_unlock
        """
        pass

    def write(self, instance=None):
        """
        Currently unimplemented
        tcl command: device_dr_shift or
        device_virtual_dr_shift if instance is defined
        """
        pass

    def read(self, instance=None):
        """
        Currently unimplemented
        tcl command: device_ir_shift or device_virtual_ir_shift if instance
        is defined
        """
        pass

    def test(self):
        """
        Currently unimplemented
        tcl command: device_run_test_idle
        """
        pass


class Hardware(object):
    """
    All functionality relating to jtag hardware (i.e., a usb-blaster)
    """
    def __init__(self, name=None):
        self.name = name

    def __str__(self):
        if self.name is None:
            return "Hardware chain does not exist"
        else:
            return self.name

    @property
    def devices(self):
        """
        currently unimplemented
        tcl command: get_device_names
        :return: list of Device
        """
        output, error = Popen(["quartus_stp", "--tcl_eval",
                               "get_device_names", "-hardware_name", self.name],
                         stdout=PIPE, stderr=PIPE).communicate()
        _device = []
        for item in output.split("\n"):
            if len(item) > 0:
                _device.append(Device(name=item, hardware_name=self.name))
        return _device