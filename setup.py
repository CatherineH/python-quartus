#!/usr/bin/env python
from sys import version_info

from os.path import join
from setuptools import setup, find_packages
from subprocess import call

from quartus import Setup


INSTALL_REQUIRES = []

py_vers_tag = '-%s.%s' % version_info[:2]


def main():
    try:
        call([join(Setup().altera_path, "quartus_stp"), "-v"])
    except Exception as error_msg:
        print("Could not execute quartus_stp for reason: "+str(error_msg)+". "
              "Have you installed Quartus Prime?")

        return
    setup(
        name="quartus",
        version="0.1",
        url="https://github.com/CatherineH/python-quartus",
        author="Catherine Holloway",
        entry_points={
        'console_scripts': [
            'pyquartus = quartus:compile_quartus',
            'pyquartus%s = quartus:compile_quartus' % py_vers_tag,
            ]},
        author_email="milankie@gmail.com",
        packages=find_packages(),
        description="A python replacement for the Tcl interface to quartus",
        install_requires=INSTALL_REQUIRES,
        zip_safe=True
    )

if __name__ == "__main__":
    main()