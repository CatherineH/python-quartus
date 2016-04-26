from subprocess import Popen, PIPE
from multiprocessing import Process
from quartus.stp_thread import StpThread


def get_hardware(stp_thread=None):
    """
    Gets a list of Hardware objects
    tcl command: get_hardware_names
    :return: list of Hardware
    """
    if stp_thread is None:
        stp_thread = StpThread()
    if stp_thread.process is None:
        stp_thread.run()
    stp_thread.process.stdin.write('get_hardware_names\n')

    _hardware = []
    output = stp_thread.process.stdin.read()
    #print(output)
    """
    for item in output.split("\n"):
        item = item.strip()
        if len(item) > 0:
            _hardware.append(Hardware(name=item))
    return _hardware
    """


class Device(object):
    """
    All functions relating to the devices. Device has its own tcl process to
    which all commands are written. This process is started in .open() and
    closed in .close().
    """
    def __init__(self, hardware_name=None, name=None):
        self.name = name
        self.hardware_name = hardware_name
        self.locked = False
        self.opened = False
        self._read_in = None
        self.process = None
        self.stp_process = None

    def __str__(self):
        if self.name is None:
            return "Device does not exist"
        else:
            return self.name

    def open(self):
        """
        Initiate communication with the device
        tcl command: open_device
        :return: True if the open operation was successful
        :rtype: bool
        """
        print("starting open")
        if self.process is None:
            self.process = StpThread()
        self.process.run()
        print("writing output")
        '''
        self.process.p.stdin.write("open_device -device_name " + self.name +
                                 " -hardware_name " + self.hardware_name + "\n")
        self.process.p.stdin.flush()
        print("flushing output")
        output = self.process.p.stdout.readline()
        print("output: "+output)
        error = self.process.p.stderr.readline()
        print("error: "+error)
        print("|"+self.name.replace("\r", "\\r").replace("\n", "\\n")+"|")

        if len(error) > 0:
            print(error)
            return 0
        else:
            self.opened = True
            return 1
        '''
        return 0

    def close(self):
        """
        Close communication with the device
        tcl command: close_device
        :return: True if the close operation was successful
        :rtype: bool
        """
        if not self.opened:
            return 1
        if self.locked:
            self.unlock()
        self.process.p.stdin.write("close_device\n")
        self.process.p.stdin.flush()
        error = self.process.p.stderr.readline()
        if len(error) > 0:
            print(error)
            return 0
        else:
            self.opened = False
            return 1

    def ready_check(self):
        """
        Make sure the device is ready for commands or read/write
        """
        if not self.opened:
            self.open()
        if not self.locked:
            self.lock()

    def parse_output(self, command):
        """
        Run a command and parse the result
        :param command: the command to run
        :type command: str
        :return: True if the command ran successfully
        :rtype: bool
        """
        self.process.p.stdin.write(command+"\n")
        self.process.p.stdin.flush()
        error = self.process.p.stderr.readline()
        output = self.process.p.stdout.readline()
        if len(error) > 0:
            self._read_in = None
            print(error)
            return 0
        else:
            self._read_in = output
            return 1

    def lock(self, timeout=10000):
        """
        Establish a read/write lock on the device
        tcl command: device_lock
        :param timeout: the amount of time in milliseconds to wait for the
        device
        :type timeout: int
        :return: True if the lock operation was successful
        :rtype: bool
        """
        if not self.opened:
            self.open()

        command = "device_lock -timeout "+str(timeout)
        print("lock command: "+command)
        self.process.p.stdin.write(command+"\n")
        self.process.p.stdin.flush()
        error = self.process.p.stderr.readline()
        if len(error) > 0:
            print(error)
            self.locked = False
            return 0
        else:
            self.locked = True
            return 1

    def unlock(self):
        """
        Unlock read/write access to the device
        tcl command: device_unlock
        :return: True if the unlock operation was successful
        :rtype: bool
        """
        if not self.opened:
            return 0
        self.process.p.stdin.write("device_unlock\n")
        self.process.p.stdin.flush()
        error = self.process.stderr.readline()
        if len(error) > 0:
            print(error)
            return 0
        else:
            self.locked = False
            return 1

    def write(self, value, instance=None, instruction=False, length=None):
        """
        Write to either the data or instruction register on either a real or
        virtual instance.
        tcl command: device_dr_shift or
        device_virtual_dr_shift if instance is defined,
        or device_ir_shift or device_virtual_ir_shift if instruction is defined
        :param value: the value to write to the data or instruction register. If
                      it is a string, it must be in a parseable format.
        :type value: str or int
        :param instance: the virtual jtag instance to write to. If undefined,
                         commands will be written to this index.
        :type instance: int
        :param instruction: If true, value will be written to the instruction
                            register instead of the data register
        :type instruction: bool
        :param length: the length of the data register. If undefined,
        the value will be guessed from the length of the input
        :type length: int
        :return: True if the write operation was successful
        :rtype: bool
        """
        self.ready_check()
        # if value is a string, parse it as either a hexadecimal or decimal
        # number
        if type(value) == 'str':
            try:
                value = int(value, 0)
            except ValueError as err_msg:
                self._read_in = None
                print("Could not parse value as hexidecimal number or "
                      "decimal: "+str(err_msg))
                return 0
        if instruction:
            if instance is not None:
                command = "device_virtual_ir_shift -instance_index " \
                          + str(instance) + " -ir_value "+str(value)
                return self.parse_output(command)
            else:
                command = "device_ir_shift -ir_value " + str(value)
                return self.parse_output(command)
        else:
            if type(value) == 'int':
                value = "{0:b}".format(value)
            if length is None:
                length = len(value)
            if instance is not None:
                command = "device_virtual_dr_shift -instance_index " \
                          + str(instance) + " -dr_value " + str(value) + \
                          " -length " + str(length)
                return self.parse_output(command)
            else:
                command = "device_dr_shift -dr_value " + str(value) + \
                          " -length " + str(length)
                return self.parse_output(command)

    def read(self):
        """
        return the last value captured from the instruction or data register
        :return: last value captured from the instruction or data register
        :rtype: str
        """
        _read_in = self._read_in
        self._read_in = None
        return _read_in

    def test(self, cycle_count=1):
        """
        Drive the JTAG controller into the Run_Test_Idle state for a number of
        cycles.
        tcl command: device_run_test_idle
        :param cycle_count: the number of clock cycles to run the test for
        :type cycle_count: int
        :return: True on success
        :rtype: bool
        """
        self.ready_check()
        self.process.p.stdin.write("device_run_test_idle -num_clocks " +
                                     str(cycle_count) + "\n")
        self.process.p.stdin.flush()
        error = self.process.p.stderr.readline()
        if len(error) > 0:
            print(error)
            return 0
        else:
            return 1


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
        tcl command: get_device_names
        :return: list of quartus.jtag.Device
        """
        command = "quartus_stp --tcl_eval get_device_names -hardware_name " \
                  +self.name
        output, error = Popen(command, shell=True, stdout=PIPE,
                              stderr=PIPE).communicate()
        _device = []
        if len(error) > 0:
            print("error: "+error+" "+str(len(error)))
            return _device
        for item in output.split("\n"):
            item = item.strip()
            if len(item) > 0:
                _device.append(Device(name=item, hardware_name=self.name))
        return _device