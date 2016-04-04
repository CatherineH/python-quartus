def get_hardware_names():
    """
    Gets a list of Hardware objects
    currently unimplemented
    tcl command: get_hardware_names
    :return: list of Hardware
    """
    pass


class Device(object):
    """
    All functions relating to the devices
    """

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
    def devices(self):
        """
        currently unimplemented
        tcl command: get_device_names
        :return: list of Device
        """
        pass