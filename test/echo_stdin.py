#from __future__ import print_function
import sys

while True:
    in_char = sys.stdin.read(1)
    out_char = ord(in_char)+1
    if in_char != '\n':
        print(chr(out_char))
