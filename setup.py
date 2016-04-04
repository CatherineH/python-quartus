#!/usr/bin/env python

from setuptools import setup, find_packages

INSTALL_REQUIRES = []

def main():
    setup(
        name="quartus",
        version="0.1",
        url="https://github.com/CatherineH/python-quartus",
        author="Catherine Holloway",
        author_email="milankie@gmail.com",
        packages=find_packages(),
        description="A python replacement for the Tcl interface to quartus",
        install_requires=INSTALL_REQUIRES
    )

if __name__ == "__main__":
    main()