import threading
from time import sleep
from subprocess import Popen, PIPE
import sys
if sys.platform == "linux" or sys.platform == "linux2":
    from select import poll



ERROR_STRINGS = ['Inconsistency detected by ld.so: dl-close.c: 762: '
                 '_dl_close: Assertion `map->l_init_called\' failed!']

class StpThread(object):
    def __init__(self):
        self.process = None
        self.poll = None

    def run(self):
        self.process = Popen(['quartus_stp', '-s'], shell=True, stdin=PIPE,
                             stdout=PIPE, stderr=PIPE)
        if sys.platform == "linux" or sys.platform == "linux2":
            self.poll = poll()
        found_number = 0
        while found_number < 3:
            output = self.process.stdout.readline()
            '''
            if type(output) == bytes:
                print("convert to string")
                output = output.decode("utf-8")
            print("output type: " + str(type(output))+" process type: "+str(type(self.process.stdin)))
            '''
            self.process.stdin.write('\n')
            if output.find('Info: *******') >= 0:
                found_number += 1
            sleep(0.1)
        print("clearing errors\n")
        # clear errors
        errors_cleared = False
        while not errors_cleared:
            print("reading errors:\n")
            output = self.process.stderr.readline()
            print("read error:\n")
            if len(output) < 4:
                errors_cleared = True
                continue
            print(str(len(output))+"\n")
            error_found = False
            for error in ERROR_STRINGS:
                if output.find(error) >= 0:
                    error_found = True
            if not error_found:
                raise Exception("Got unrecognized error from TCL: "+output)


