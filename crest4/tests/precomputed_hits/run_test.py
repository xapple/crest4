#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Script to run the `precomputed_hits` integration test.
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
def test_precomputed_hits():
    # The input fasta #
    fasta = this_dir.find('*.fasta')
    # The input BLAST hits #
    hits = this_dir.find('*.hits')
    # The output directory #
    output_dir = this_dir + 'results/'
    output_dir.remove()
    # Create object #
    c = Classify(fasta       = fasta,
                 search_hits = hits,
                 output_dir  = output_dir,
                 num_threads = True)
    # Patch the search method so it can't be called #
    c.search = lambda x: x/0
    # Run it #
    c()
    # Check that the results are good #
    assert c.queries_by_id['Kocuria'].taxonomy[0] == "Micrococcaceae"
    assert c.queries_by_id['Marmoricola'].taxonomy[0] == "Nocardioidaceae"
    # Return #
    return c

###############################################################################
if __name__ == '__main__':
    classify = test_precomputed_hits()