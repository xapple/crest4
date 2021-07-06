#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Script to run the `ncbi_two_sequences` integration test.
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
def test_with_otu_table():
    # The input fasta #
    fasta = this_dir.find('*.fasta')
    # The input table #
    otu_table = this_dir.find('*.tsv')
    # The output directory #
    output_dir = this_dir + 'results/'
    output_dir.remove()
    # Create object #
    c = Classify(fasta       = fasta,
                 output_dir  = output_dir,
                 num_threads = True,
                 otu_table   = otu_table)
    # Run it #
    c()
    # Check that the results are good #
    assert all(c.otu_info.otus_by_rank['river'].array == [51, 10])
    assert all(c.otu_info.otus_by_rank['lake'].array  == [102, 50])
    assert all(c.otu_info.otus_by_rank['ocean'].array == [3, 200])
    # Return #
    return c

###############################################################################
if __name__ == '__main__':
    classify = test_with_otu_table()
