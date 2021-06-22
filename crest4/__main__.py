#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Written by Lucas Sinclair.
GNUv3 Licensed.
Contact at www.sinclair.bio
Created in May 2021.
"""

# Use the optmagic library to make a command line tool automatically #
from optmagic import OptMagic

# The main object of our package #
from crest4 import Classify

# The main function to run when we are called #
def main(): return OptMagic(Classify)()

# Execute when run, not when imported #
if __name__ == "__main__": main()