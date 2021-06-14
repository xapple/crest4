#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Script to run the `actualize_database` unittest.
"""

# Built-in modules #

# First party modules #

# Third party modules #

# Internal modules #
from crest4.databases import metadata, silvamod128

###############################################################################
def test_download_metadata():
    urls = metadata.db_urls
    assert urls

def test_blast_index():
    db = silvamod128.blast_db
    assert db

def test_vsearch_index():
    db = silvamod128.vsearch_db
    assert db

###############################################################################
if __name__ == '__main__':
    test_download_metadata()
    test_blast_index()
    test_vsearch_index()