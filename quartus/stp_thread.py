import threading
import subprocess


class StpThread(threading.Thread):
    def __init__(self):
        self.stdout = None
        self.stderr = None
        threading.Thread.__init__(self)

    def run(self):
        self.p = subprocess.Popen(['quartus_stp', '-s'])\
            #                stdout=subprocess.PIPE,
            #                 stdin=subprocess.PIPE, stderr=subprocess.PIPE)
