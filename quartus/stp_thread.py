import threading
from time import sleep
from subprocess import Popen, PIPE


class StpThread(object):
    def __init__(self):
        self.p = None

    def run(self):
        self.p = Popen(['quartus_stp', '-s'], stdin=PIPE, stdout=PIPE)
        found_number = 0
        while found_number < 3:
            output = self.p.stdout.readline()
            self.p.stdin.write('\n')
            if output.find('Info: *******') >= 0:
                found_number += 1
            sleep(0.1)

