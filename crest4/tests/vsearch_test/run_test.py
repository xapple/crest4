#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Script to run the `vsearch` integration test.
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
def test_vsearch(verbose=True):
    # The input fasta #
    fasta = this_dir.find('*.fasta')
    # The output directory #
    output_dir = this_dir + 'results/'
    output_dir.remove()
    # Create object #
    c = Classify(fasta       = fasta,
                 output_dir  = output_dir,
                 search_algo = 'vsearch',
                 num_threads = True)
    # Run it #
    c()
    # This test is sometimes failing, more prints for debugging #
    if verbose:
        print("c.queries_by_id --------")
        print(c.queries_by_id)
        print("c.queries[0].taxonomy --------")
        print(c.queries[0].taxonomy)
        print("c.queries[1].taxonomy --------")
        print(c.queries[1].taxonomy)
    # Check that the results are good #
    assert c.queries[0].taxonomy[0] == "Micrococcaceae"
    assert c.queries_by_id['Kocuria'].taxonomy[0] == "Micrococcaceae"
    # Here with VSEARCH we end up one level above as compared to BLAST #
    assert c.queries_by_id['Marmoricola'].taxonomy[0] == "Propionibacteriales"
    # Return #
    return c

###############################################################################
if __name__ == '__main__':
    classify = test_vsearch()
