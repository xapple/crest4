#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Script to run the `no_hits_sequence` integration test.
"""

# Built-in modules #
import inspect

# First party modules #
from autopaths import Path

# Third party modules #

# Internal modules #
from crest4 import Classify

# Get the current directory of this python script #
this_file = Path((inspect.stack()[0])[1])
this_dir  = this_file.directory

###############################################################################
def test_no_hits_sequence():
    # The input fasta #
    fasta = this_dir.find('*.fasta')
    # The output directory #
    output_dir = this_dir + 'results/'
    output_dir.remove()
    # Create object #
    c = Classify(fasta       = fasta,
                 output_dir  = output_dir,
                 num_threads = True)
    # Run it #
    c()
    # Check there was no hits for the second sequence #
    expected = "homopolymer\tNo hits"
    got = c.out_file.lines[1]
    assert got == expected
    # Return #
    return c

###############################################################################
if __name__ == '__main__':
    classify = test_no_hits_sequence()