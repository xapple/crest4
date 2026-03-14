#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Script to run the `score_drop_change` integration test.

Original issue #10:
https://github.com/xapple/crest4/issues/10
"""

# Built-in modules #
import inspect, subprocess, sys

# First party modules #
from autopaths import Path

# Get the current directory of this python script #
this_file = Path((inspect.stack()[0])[1])
this_dir  = this_file.directory

###############################################################################
def test_min_score():
    # The input fasta #
    fasta = this_dir.find('*.fasta')
    # The output directory #
    output_dir = this_dir + 'results/'
    output_dir.remove()
    # Call via the command line tool #
    result = subprocess.run([sys.executable,
                             '-m',            'crest4',
                             '--fasta',       str(fasta),
                             '--output_dir',  str(output_dir),
                             '--min_score',   '2.5'],
                            check=True)
    # Check that the results were created #
    created_file = output_dir + 'assignments.txt'
    assert created_file
    # Return #
    return result

###############################################################################
if __name__ == '__main__':
    test_min_score()