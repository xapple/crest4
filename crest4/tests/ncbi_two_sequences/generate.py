#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Written by Lucas Sinclair.
GNUv3 Licensed.
Contact at www.sinclair.bio
Created in May 2021.
"""

# Built-in modules #
import inspect

# First party modules #
from seqsearch.databases.download import acc_to_fasta
from fasta import FASTA
from autopaths import Path

# Third party modules #
from Bio.SeqRecord import SeqRecord
from Bio.Seq import Seq

# Get the current directory of this python script #
this_file = Path((inspect.stack()[0])[1])
this_dir  = this_file.directory

# Random sequences from NCBI #
# Taken from https://www.ncbi.nlm.nih.gov/refseq/targetedloci/16S_process/ #
accessions = {
    'NR_171545.1': "Bacteria; Actinobacteria; Micrococcales; Micrococcaceae; Kocuria",
    'NR_171544.1': "Bacteria; Actinobacteria; Propionibacteriales; Nocardioidaceae; Marmoricola"
}

###############################################################################
if __name__ == '__main__':
    # Download from the web #
    sequences = acc_to_fasta(accessions.keys())

    # Parse them #
    records = [(seq['TSeq_sequence'],
                ' '.join(seq['TSeq_defline'].split(' ')[:3]))
               for seq in sequences]

    # Make biopython objects out of them #
    records = [SeqRecord(Seq(seq), id=name, description='')
               for seq, name in records]

    # Write to a new file #
    fasta = FASTA(this_dir + 'two_seqs.fasta')
    fasta.write(records)