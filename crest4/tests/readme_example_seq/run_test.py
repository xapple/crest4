#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Script to run the `readme_example_seq` integration test.
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
def test_readme_example_seq():
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
    # Check that the results are good #
    assert c.queries[0].taxonomy[0] == "Synechococcales"
    # Return #
    return c

###############################################################################
if __name__ == '__main__':
    classify = test_readme_example_seq()