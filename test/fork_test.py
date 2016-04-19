# run the echo process in the background, and communicate with it
from time import sleep
from subprocess import Popen, PIPE


process = Popen(['quartus_stp', '-s'], stdin=PIPE, stdout=PIPE)
current_value = 0
found_number = 0
while found_number < 3:
    output = process.stdout.readline()
    process.stdin.write('\n')
    if output.find('Info: *******') >= 0:
        found_number += 1
    sleep(0.1)

print "got prompt"

process.stdin.write('get_hardware_names\n')
while True:
    output = process.stdout.readline().replace("tcl>", "")
    if output.find("ERROR") >= 0:
        print "got error: "+output.replace("ERROR:", "")
    else:
        print "got line: "+output
