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
    assert metadata.db_urls

def test_download_database():
    silvamod128.download()
    assert silvamod128.downloaded

###############################################################################
if __name__ == '__main__':
    test_download_metadata()
    test_download_database()