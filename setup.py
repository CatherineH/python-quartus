#!/usr/bin/env python

from setuptools import setup, find_packages
from subprocess import call
import os

print os.environ["PATH"]

INSTALL_REQUIRES = []


def main():
    try:
        call(["quartus_stp", "-v"], shell=True)
    except Exception as error_msg:
        print("Could not execute quartus_stp for reason: " + str(error_msg) +
              ". "
              "Have you installed Quartus "
              "Prime and added the executables folder to %PATH%?")
        return
    setup(
        name="quartus",
        version="0.1",
        url="https://github.com/CatherineH/python-quartus",
        author="Catherine Holloway",
        author_email="milankie@gmail.com",
        packages=find_packages(),
        description="A python replacement for the Tcl interface to quartus",
        install_requires=INSTALL_REQUIRES,
        zip_safe=True
    )

if __name__ == "__main__":
    main()