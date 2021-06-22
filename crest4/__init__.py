#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
The `crest4` python package can automatically assign taxonomic names to
DNA sequences obtained from environmental sequencing.
"""

# Special variables #
__version__ = '4.0.23'

# Constants #
project_url = 'https://github.com/xapple/crest4'

# Expose our main object at the module level
# So that you can just do 'from crest4 import Classify' later
from .classify import Classify