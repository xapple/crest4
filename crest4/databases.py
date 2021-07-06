#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Written by Lucas Sinclair.
GNUv3 Licensed.
Contact at www.sinclair.bio
Created in May 2021.
"""

# Built-in modules #
import os, json

# Internal modules #

import crest4

# First party modules #
from autopaths.dir_path import DirectoryPath
from plumbing.cache     import property_cached
from plumbing.scraping  import download_from_url, retrieve_from_url
from seqsearch.search.blast   import BLASTdb
from seqsearch.search.vsearch import VSEARCHdb

# Third party modules #
from ete3 import Tree

###############################################################################
class CrestMetadata:
    """
    The databases that `crest4` needs are slightly too large to be distributed
    with the source tarball on PyPI. Therefore, we host them on a separate
    server. Currently this is S3 on AWS.

    Over the course of years however these servers might be shutdown.
    To avoid this inconvenience, instead of hard-coding the server address here
    in the source file, we instead maintain a metadata file.

    This metadata file contains the up-to-date URLs of the databases
    to download. It is placed in the github repository and only the location
    of the metadata file is hardcoded into the source code.

    This enables updating the URLs without having to issue a new release of
    `crest4`.

    A good read on this subject is the following:

    https://www.dampfkraft.com/code/distributing-large-files-with-pypi.html
    """

    # The location of the metadata file is hardcoded #
    base_url  = "https://raw.githubusercontent.com/xapple/"
    repo_path = "crest4/master/crest4/crest4_db_urls.json"

    # This will always retrieve the raw content of the latest version #
    metadata_url = base_url + repo_path

    # To see the HTML version on github simply head to this address instead:
    # https://github.com/xapple/crest4/blob/master/crest4/crest4_db_urls.json

    @property_cached
    def db_urls(self):
        """
        Once the `Metadata` object is created simply access it like this:
        >>> print(metadata.db_urls['silvamod']['url'])
        """
        # Download the gist #
        content = retrieve_from_url(self.metadata_url)
        # Parse it #
        data = json.loads(content)
        # Validate it #
        assert list(data) == ['crest4_databases']
        # Return it #
        return data['crest4_databases']

# The metadata should be very rarely updated -- we create a singleton #
metadata = CrestMetadata()

###############################################################################
class CrestDatabase:
    """
    This object represents a database of taxonomically curated DNA sequences
    that was subsequently specifically formatted for use with `crest4`.
    It comes with a FASTA file, as well as a tree.
    """

    # Default location for a database #
    default_dir = os.path.expanduser('~/.crest4/')

    # The environment variable that the user can set #
    environ_var = "CREST4_DIR"

    def __init__(self, short_name, long_name, base_dir=None):
        """
        The user can specify a path pointing to a directory that contains all
        the required files, and having the same prefix as the directory name.
        It must include the database FASTA file as well as the `.map` and
        `.names` file.
        """
        # Base required attributes #
        self.short_name = short_name
        self.long_name = long_name
        # If the user specifies a base_dir, then no need to download #
        if base_dir is not None:
            self.downloaded = True
        # If the user doesn't specify a base_dir path, then we should
        # determine where the actual files will be located on disk and
        # check if the user has set the special environment variable.
        if base_dir is None:
            base_dir = os.environ.get(self.environ_var, self.default_dir)
        # Convert to a DirectoryPath #
        self.base_dir = DirectoryPath(base_dir)

    def __repr__(self):
        """A simple representation of this object to avoid memory addresses."""
        return "<%s object at '%s'>" % (self.__class__.__name__, self.path)

    @property
    def tag(self):
        """
        Some methods will look for the `tag` attribute to print the name of the
        database.
        """
        return self.short_name

    @property
    def tarball(self):
        """Determine where the database `.tar.gz` will be located on disk."""
        return self.base_dir + self.short_name + '.tar.gz'

    @property
    def path(self):
        """The path to the FASTA file."""
        return self.base_dir + self.short_name + '/' + \
               self.short_name + '.fasta'

    @property_cached
    def downloaded(self):
        """
        Determine if the database has been downloaded to disk and uncompressed
        previously. Returns `True` or `False`.
        """
        # Check if the tree is there and not empty #
        return bool(self.path.replace_extension('tre'))

    @property
    def url(self):
        """
        Retrieve the URL of the database file to download by first downloading
        a metadata file (see the `Metadata` class above).
        """
        return metadata.db_urls[self.short_name]['url']

    def download(self):
        """
        Download the database file, uncompress it, and save it to disk.
        """
        # Compose a message so the user knows why it's taking time #
        message = "The database '%s' has not been downloaded yet." \
                  " This process will start now and might take some time" \
                  " depending on your internet connection. Please be" \
                  " patient. The result will be saved to '%s'. You can" \
                  " override this by setting the $%s environment variable."
        message = message % (self.short_name, self.base_dir, self.environ_var)
        # Display the message with style in a box #
        from plumbing.common import rich_panel_print
        rich_panel_print(message, "Large Download")
        # Show a progress bar a bit like wget #
        download_from_url(self.url,
                          destination = self.tarball,
                          uncompress  = False,
                          user_agent  = "crest4 v" + crest4.__version__,
                          stream      = True,
                          progress    = True,
                          desc        = self.short_name)
        # Uncompress #
        self.tarball.untargz_to(self.base_dir)
        # Remove tarball #
        self.tarball.remove()
        # Remove macOS attribute files that get bundled in the tar #
        for path in self.base_dir.flat_files:
            if path.name.startswith("._"): path.remove()
        # Check it worked #
        del self.downloaded
        assert self.downloaded

    #--------------------------- Specific Indexes ----------------------------#
    @property_cached
    def blast_db(self):
        """
        Return a `BLASTDb` object that can be used for the sequence
        similarity search.
        """
        # Download the database if it has not been done already #
        if not self.downloaded: self.download()
        # Create the database object #
        db = BLASTdb(self.path, seq_type='nucl')
        # Create the database with `mkblastdb` if it's not made already #
        db.create_if_not_exists(verbose=True)
        # Return #
        return db

    @property_cached
    def vsearch_db(self):
        """
        Return a `VSEARCHdb` object that can be used for the sequence
        similarity search.
        """
        # Download the database if it has not been done already #
        if not self.downloaded: self.download()
        # Create the database object #
        db = VSEARCHdb(self.path.replace_extension('udb'))
        # Create the database with `vsearch` if it's not made already #
        db.create_if_not_exists(verbose=True)
        # Return #
        return db

    #--------------------------- Loading the tree ----------------------------#
    @property_cached
    def tree(self):
        """
        Using the `.tre` file, we return a N-ary tree in memory.
        Every node is characterised by a number. For instance between
        1 and 32477.
        """
        # Load the tree with ete3 #
        tree = Tree(self.path.replace_extension('tre'), format=8)
        # Add information from the `map` file #
        return tree

    @property_cached
    def node_to_name(self):
        """
        Using the `.names` file, we return a dictionary linking node numbers to
        a tuple of species names and a minimum similarity fraction like 0.97.
        Example: 51 -> (Proteobacteria, 0.8)
        """
        # Get the path of the file #
        path = self.path.replace_extension('names')
        # Define how to process each line #
        def parse_lines(lines):
            for line in lines:
                if line.startswith('#') or not line: continue
                num, name, frac = line.strip().split(',')
                yield num, (name, frac)
        # Create a dictionary #
        with open(path, 'rt') as handle: return dict(parse_lines(handle))

    @property_cached
    def acc_to_node(self):
        """
        Using the `.map` file, we return a dictionary linking accession numbers
        to node numbers.
        Example: HQ191339 -> 28386
        """
        # Get the path of the file #
        path = self.path.replace_extension('map')
        # Define how to process each line #
        def parse_lines(lines):
            for line in lines:
                if line.startswith('#') or not line: continue
                num, name = line.strip().split(',')
                yield name, num
        # Create a dictionary #
        with open(path, 'rt') as handle: return dict(parse_lines(handle))

    #--------------------------- Extra information ----------------------------#
    @property
    def rank_names(self):
        return ['Root',           # 0
                'Genome',         # 1 (This is for instance mitochondria)
                'Domain',         # 2
                'Superkingdom',   # 3
                'Kingdom',        # 4 (This is also called Superphylum)
                'Phylum',         # 5
                'Class',          # 6
                'Order',          # 7
                'Family',         # 8
                'Genus',          # 9
                'Species']        # 10

###############################################################################
class Silvamod128(CrestDatabase):
    """
    Represents the old silvamod database.
    """

    short_name = 'silvamod128'
    long_name  = 'Silva version 128 modified for CREST'

###############################################################################
class Silvamod138(CrestDatabase):
    """
    Represents the new silvamod database.
    """

    short_name = 'silvamod138'
    long_name  = 'Silva version 138 modified for CREST'

###############################################################################
# As our databases should only be stored on disk once, so we have singletons #
silvamod128 = CrestDatabase('silvamod128',
                            'Silva version 128 modified for CREST')

silvamod138 = CrestDatabase('silvamod138',
                            'Silva version 138 modified for CREST')