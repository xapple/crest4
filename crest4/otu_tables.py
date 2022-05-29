#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Written by Lucas Sinclair.
GNUv3 Licensed.
Contact at www.sinclair.bio
Created in May 2021.
"""

# Built-in modules #
from collections import defaultdict

# First party modules #
from plumbing.cache import property_cached

# Third party modules #
import pandas

###############################################################################
class InfoFromTableOTUs:
    """
    This class accepts a path to an OTU table as input.
    It will parse the table, along with the taxonomic assignments
    from the `Classify` object, and it will produce two extra output files.
    """

    def __init__(self, classify, otu_table):
        # A reference to the parent object #
        self.classify = classify
        # Path to a CSV or TSV file #
        self.otu_table = otu_table

    def __repr__(self):
        """A simple representation of this object to avoid memory addresses."""
        return "<%s object on '%s'>" % (self.__class__.__name__, self.otu_table)

    @property_cached
    def format(self):
        """
        Automatically detect the format between "TSV" or "CSV" and return the
        appropriate separator character. By default we will return a tab.
        """
        if self.otu_table.filename.split('.')[-1] == 'csv':
            return ','
        return '\t'

    @property_cached
    def otus_df(self):
        """Load the otu_table file as a pandas `DataFrame`."""
        # Load from a text file #
        df = pandas.read_csv(str(self.otu_table), sep=self.format, index_col=0)
        # We only want the very first part of the IDs #
        df.index = df.index.map(lambda s: s.split()[0])
        # Return #
        return df

    @property_cached
    def otus_by_rank(self):
        """The first output file where cumulativeness is turned off."""
        return self(cumulative=False)

    @property_cached
    def otus_cumulative(self):
        """The second output file where cumulativeness is turned on."""
        return self(cumulative=True)

    def check_id_match(self):
        """
        Check that all the IDs in the OTU table given by the user match the
        ones in the FASTA file.
        """
        for i, otu_counts in self.otus_df.iterrows():
            # The name or id of the current OTU #
            name = otu_counts.name
            if name not in self.classify.queries_by_id:
                msg = "The sequence named '%s' in the table located at '%s'" \
                      " does not appear in the FASTA file provided at '%s'."
                msg = msg % (name, self.otu_table, self.classify.fasta)
                raise ValueError(msg)

    def __call__(self, cumulative=False):
        # Let's first check all the IDs are found #
        self.check_id_match()
        # An empty pandas Series with each sample name and just zeros #
        empty_samples = pandas.Series(0, index=self.otus_df.columns)
        # Build a empty new dataframe from a dictionary of empty series #
        result = defaultdict(lambda: empty_samples.copy())
        # Loop over every OTU in the user supplied table #
        for i, otu_counts in self.otus_df.iterrows():
            # The name or id of the current OTU #
            otu_name = otu_counts.name
            # Get the assignment of current OTU from our classification #
            tax = self.classify.queries_by_id[otu_name].taxonomy
            # By default the root is at the end #
            tax = list(reversed(tax))
            # Make a string #
            tax_name = '; '.join(tax)
            # Add the current counts to that particular taxonomy #
            result[tax_name] += otu_counts
            # If we have the cumulative option then propagate up the tree #
            if cumulative:
                for step in range(1, len(tax)):
                    tax_name = '; '.join(tax[0:-step])
                    result[tax_name] += otu_counts
        # Convert to a DataFrame #
        result = pandas.DataFrame(result).T
        # Have the assignment as a separate column and not as an index #
        result = result.reset_index()
        result = result.rename(columns = {'index': 'taxonomy'})
        # Add the rank column that tells the user if it's a genus or a family #
        rank_names  = self.classify.database.rank_names
        tax_to_rank = lambda t: rank_names[len(t.split(';')) - 1]
        ranks       = result.taxonomy.apply(tax_to_rank)
        result.insert(loc=0, column='rank', value=ranks)
        # Sort the table by the taxonomy string #
        result = result.sort_values(by=['taxonomy'])
        # Return #
        return result
