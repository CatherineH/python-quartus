# run the echo process in the background, and communicate with it
#from time import sleep
from subprocess import Popen, PIPE

process = Popen(['python', 'echo_stdin.py'], stdin=PIPE)
