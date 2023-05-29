#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Script to run the `actualize_database` unittest.
"""

# Built-in modules #
import os

# First party modules #

# Third party modules #

# Internal modules #
from crest4.databases import metadata, silvamod138pr2, CrestDatabase

# Constants #
env_val = os.environ.get(CrestDatabase.environ_var)

###############################################################################
def test_download_metadata():
    urls = metadata.db_urls
    assert urls

def test_blast_index():
    db = silvamod138pr2.blast_db
    assert db

def test_vsearch_index():
    db = silvamod138pr2.vsearch_db
    assert db

###############################################################################
if __name__ == '__main__':
    # Some debug information #
    print("Default directory: ",         CrestDatabase.default_dir)
    print("Environment variable: ",      CrestDatabase.environ_var)
    print("Environment value: ",         env_val)
    print("silvamod138pr2 path: ",       silvamod138pr2.path)
    print("silvamod138pr2 exists: ",     silvamod138pr2.path.exists)
    print("silvamod138pr2 downloaded: ", silvamod138pr2.downloaded)
    print("silvamod138pr2 URL: ",        silvamod138pr2.url)
    # Run the three tests #
    test_download_metadata()
    test_blast_index()
    test_vsearch_index()