#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Script to run the `cmd_line_tool` integration test.
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
def test_cmd_line_tool():
    # The input fasta #
    fasta = this_dir.find('*.fasta')
    # The output directory #
    output_dir = this_dir + 'results/'
    output_dir.remove()
    # Call command line tool #
    import sh
    this_python = sh.Command(sys.executable)
    result = this_python('-m',             'crest4',
                         '--fasta',        fasta,
                         '--output_dir',   output_dir,
                         '--num_threads',  'True')
    # Check that the results were created #
    created_file = output_dir + 'assignments.txt'
    assert created_file
    # Return #
    return result

###############################################################################
if __name__ == '__main__':
    command = test_cmd_line_tool()