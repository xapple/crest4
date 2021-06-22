#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Written by Lucas Sinclair.
GNUv3 Licensed.
Contact at www.sinclair.bio
Created in May 2021.
"""

# Built-in modules #
import multiprocessing

# Internal modules #
import crest4.databases
from crest4.query import Query

# First party modules #
from plumbing.cache      import property_cached
from seqsearch.search    import SeqSearch
from fasta               import FASTA
from autopaths.file_path import FilePath
from autopaths.dir_path  import DirectoryPath

###############################################################################
class Classify:
    """
    This is the main object offered by the `crest4` package.
    It enables you to automatically assign taxonomic names to DNA sequences
    obtained from environmental sequencing.

    After creating a new instance of a `Classify` object, you can simply call
    it to have it process your input data and generate the assignments output
    file. Examples are included in the README.md file of this package or
    directly on the github page at:

    https://github.com/xapple/crest4/
    """

    def __init__(self,
                 fasta,
                 search_algo = 'blast',
                 num_threads = 1,
                 search_db   = 'silvamod128',
                 output_dir  = None,
                 search_hits = None,
                 min_score   = None,
                 score_drop  = 2.0,
                 min_smlrty  = True,
                 ):
        """
        Args:

            fasta: The path to a single FASTA file as a string.
                   These are the sequences that will be taxonomically
                   classified.

            search_algo: The algorithm used for the sequence similarity search
                         that will be run to match the sequences against the
                         database chosen. Either `blast` or `vsearch`. No
                         other values are currently supported. By default
                         `blast`.

            num_threads: The number of processors to use for the sequence
                         similarity search. By default parallelism is turned
                         off and this value is 1. If you pass the value `True`
                         we will run as many processes as there are CPUs but
                         no more than 32.

            search_db: The database used for the sequence similarity search.
                       Either `silvamod128` or `greengenes`. No other values
                       are currently supported. By default `silvamod128`.

            output_dir: The directory into which all the classification
                        results will be written to. This defaults to a
                        directory with the same name as the original FASTA
                        file and a `.crest4` suffix appended.

            search_hits: The path where the search results will be stored.
                         This defaults to the output directory. However,
                         if the search operation has already been completed
                         before hand, specify the path here to skip the
                         sequence similarity search step and go directly to
                         the taxonomy step.

            min_score: The minimum bit-score for a search hit to be considered
                       when using BLAST as the search algorithm. All hits below
                       this score are ignored. When using VSEARCH, this value
                       instead indicates the minimum identity between two
                       sequences for the hit to be considered.
                       The default is `155` for BLAST and `0.75` for VSEARCH.

            score_drop: Determines the range of hits to retain and the range
                        to discard based on a drop in percentage from the score
                        of the best hit. Any hit below the following value:
                        "(100 - score_drop)/100 * best_hit_score" is ignored.
                        By default `2.0`.

            min_smlrty: Determines if the minimum similarity filter is turned
                        on or off. Pass the value `False` to turn it off.
                        The minimum similarity filter prevents classification
                        to higher ranks when a minimum rank-identity is not met.
                        By default `True`.
        """
        # Save attributes #
        self.fasta       = fasta
        self.search_algo = search_algo
        self.num_threads = num_threads
        self.search_db   = search_db
        self.output_dir  = output_dir
        self.search_hits = search_hits
        self.min_score   = min_score
        self.score_drop  = score_drop
        self.min_smlrty  = min_smlrty
        # Assign default values and change others #
        self.transform()
        # Validate attributes #
        self.validate()

    def transform(self):
        """
        This method will replace empty attributes with defaults when this is
        needed and will convert others to proper types.
        """
        # The fasta should be a FASTA object #
        if self.fasta is not None:
            self.fasta = FASTA(self.fasta)
        # The search hits is a file somewhere #
        if self.search_hits is not None:
            self.search_hits = FilePath(self.search_hits)
            self.search_hits.must_exist()
        # Default for the number of threads #
        if not isinstance(self.num_threads, int):
            if self.num_threads is True:
                self.num_threads = min(multiprocessing.cpu_count(), 32)
            elif self.num_threads is False:
                self.num_threads = 1
            elif self.num_threads.lower() == 'true':
                self.num_threads = min(multiprocessing.cpu_count(), 32)
        # Default for the output directory #
        if self.output_dir is None:
            self.output_dir = DirectoryPath(self.fasta + '.crest4/')
        # Default for the search hits file #
        if self.search_hits is None:
            self.search_hits = self.output_dir + 'search.hits'
        # Default for the minimum score #
        if self.min_score is None:
            if self.search_algo == 'blast':
                self.min_score = 155
            if self.search_algo == 'vsearch':
                self.min_score = 0.75

    def validate(self):
        """
        This method will raise an Exception if any of the arguments passed by
        the user are illegal.
        """
        # The fasta should exist if passed #
        if self.fasta is not None:
            self.fasta.must_exist()
        # Either the FASTA file or the hits file has to contain something #
        if not self.fasta and not self.search_hits:
            msg = "Neither the FASTA file at '%s' nor the search hits file at" \
                  " '%s' contain any data. Cannot proceed."
            raise Exception(msg % (self.fasta, self.search_hits))
        # Check the search algorithm #
        if self.search_algo not in ('blast', 'vsearch'):
            msg = "The search algorithm '%s' is not supported."
            raise ValueError(msg % self.search_algo)
        # Check the search database #
        if self.search_db not in ('silvamod128', 'greengenes'):
            msg = "The search database '%s' is not supported."
            raise ValueError(msg % self.search_db)
        # Check the minimum score value above zero #
        if self.min_score < 0.0:
            msg = "The minimum score cannot be smaller than zero ('%s')."
            raise ValueError(msg % self.min_score)
        # Check the minimum score value below zero #
        if self.min_score > 1.0:
            if self.search_algo == 'vsearch':
                msg = "The minimum score cannot be more than 1.0 when" \
                      " using VSEARCH ('%s') because it represents the" \
                      " the minimum identity between two sequences."
                raise ValueError(msg % self.min_score)
        # Check the score drop value #
        if self.score_drop < 0.0:
            msg = "The score drop value cannot be smaller than zero ('%s')."
            raise ValueError(msg % self.min_score)
        if self.score_drop > 100.0:
            msg = "The score drop value cannot be over 100 ('%s')."
            raise ValueError(msg % self.min_score)

    def __repr__(self):
        """A simple representation of this object to avoid memory addresses."""
        return "<%s object on '%s'>" % (self.__class__.__name__, self.fasta)

    @property_cached
    def database(self):
        """Retrieve the database object that the user has selected."""
        return getattr(crest4.databases, self.search_db)

    #------------------------------ Searching --------------------------------#
    @property_cached
    def seqsearch(self):
        """
        An object representing the sequence similarity search.
        Makes use of the `seqsearch` module. For reference:
        * Setting `-outfmt` to 5 means XML output.
        * Setting `-outfmt` to 6 means tabular output.
        * Setting `-outfmt` to 7 means tabular output with comments.
        """
        # Initialize #
        params = {}
        # If the user chose BLAST then we have to specify tabular output #
        if self.search_algo == 'blast':
            params = {'-outfmt': '7 qseqid sseqid bitscore length nident'}
        # In case the user chose VSEARCH we specify the minimum identify #
        if self.search_algo == 'vsearch':
            params = {'-id': self.min_score}
        # Build the object
        return SeqSearch(input_fasta = self.fasta,
                         database    = self.database,
                         seq_type    = 'nucl',
                         algorithm   = self.search_algo,
                         filtering   = {'max_targets': 100},
                         num_threads = self.num_threads,
                         out_path    = self.search_hits,
                         params      = params)

    def search(self):
        """A method to launch the sequence similarity search."""
        # Launch the search algorithm #
        return self.seqsearch.run()

    #----------------------------- Assigning ---------------------------------#
    @property_cached
    def score_frac(self):
        """
        Using the parameter `self.score_drop` which is a percentage (e.g. 2)
        indicating a drop, we compute the minimum remaining amount of score
        allowed, as a fraction (e.g. 0.98).
        """
        return 1 - (self.score_drop / 100)

    @property_cached
    def queries(self):
        """
        A list containing one Query object per sequence that was originally
        inputted. Use these objects to access the taxonomic assignments.
        """
        # Check if the search has been done already #
        if not self.seqsearch: self.search()
        # Iterate on the sequence search results #
        return [Query(self, query) for query in self.seqsearch.results]

    #------------------------------- Outputs ---------------------------------#
    @property_cached
    def out_file(self):
        """
        The path to the file that will contain the taxonomic assignments
        for every sequence.
        """
        return self.output_dir + "assignments.txt"

    def __call__(self):
        """Generate outputs."""
        # Iterate #
        self.out_file.writelines(query.tax_string for query in self.queries)
        # Print a success message #
        msg = "Classification ran successfully. Results are placed in '%s'"
        print(msg % self.out_file)
        # Return #
        return self.out_file
