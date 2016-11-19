#!/usr/bin/env python
from sys import version_info

from os import system
from os.path import isdir
from os.path import join
from setuptools import setup, find_packages, Command
from shutil import rmtree
from subprocess import call



INSTALL_REQUIRES = []

py_vers_tag = '-%s.%s' % version_info[:2]


class CleanCommand(Command):
    """Custom clean command to tidy up the project root."""
    user_options = []

    def initialize_options(self):
        pass

    def finalize_options(self):
        pass

    def run(self):
        if isdir('build'):
            rmtree('build')
        if isdir('dist'):
            rmtree('dist')
        if isdir('quartus.egg-info'):
            rmtree('quartus.egg-info')


def main():
    setup(
        name="quartus",
        version="0.1",
        url="https://github.com/CatherineH/python-quartus",
        author="Catherine Holloway",
        entry_points={
        'console_scripts': [
            'pyquartus = quartus:compile_quartus',
            #'pyquartus = quartus:say_hello',
            'pyquartus%s = quartus:compile_quartus' % py_vers_tag,
            ]},
        author_email="milankie@gmail.com",
        packages=find_packages(),
        description="A python replacement for the Tcl interface to quartus",
        install_requires=INSTALL_REQUIRES,
        zip_safe=True,
        cmdclass={
            'clean': CleanCommand,
        }
    )

if __name__ == "__main__":
    main()