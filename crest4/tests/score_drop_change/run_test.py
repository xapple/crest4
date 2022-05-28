#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Script to run the `score_drop_change` integration test.
"""

# Built-in modules #
import inspect, sys

# First party modules #
from autopaths import Path

# Third party modules #

# Internal modules #

# Get the current directory of this python script #
this_file = Path((inspect.stack()[0])[1])
this_dir  = this_file.directory

###############################################################################
def test_score_drop_change():
    # The input fasta #
    fasta = this_dir.find('*.fasta')
    # The output directory #
    output_dir = this_dir + 'results/'
    output_dir.remove()
    # Get the path of the current python executable #
    import sh
    this_python = sh.Command(sys.executable)
    # Call via the command line tool #
    result = this_python('-m',            'crest4',
                         '--fasta',       fasta,
                         '--search_db',   'silvamod138',
                         '--output_dir',  output_dir,
                         '--score_drop',  '1')
    # Check that the results were created #
    created_file = output_dir + 'assignments.txt'
    assert created_file
    # Return #
    return result

###############################################################################
if __name__ == '__main__':
    command = test_score_drop_change()