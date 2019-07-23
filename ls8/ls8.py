#!/usr/bin/env python3

"""Main."""

from sys import argv
from cpu import *

if __name__ == '__main__':
    cpu = CPU()
    cpu.load(argv[1])
    cpu.run()