#from __future__ import print_function
from sys import platform as _platform
if _platform == "linux" or _platform == "linux2":
    import sys
elif _platform == "win32":
    import msvcrt

while True:
    if _platform == "linux" or _platform == "linux2":
        in_char = sys.stdin.read(1)
    elif _platform == "win32":
        in_char = msvcrt.getch()
    if len(in_char) == 1:
        out_char = ord(in_char)+1
        if in_char != '\n':
            print(chr(out_char))
