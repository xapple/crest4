#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
The `crest4` python package can automatically assign taxonomic names to
DNA sequences obtained from environmental sequencing.

The README and source code are located at:

https://github.com/xapple/crest4
"""

# Special variables #
__version__ = '4.3.7'

# Constants #
project_url = 'https://github.com/xapple/crest4'

# Expose our main object at the module level
# So that you can just do `from crest4 import Classify` later
from .classify import Classify

# After sh==1.14.3 the object returned changed #
import sh
sh_version = int(sh.__version__.split('.')[0])
if sh_version > 1: sh = sh.bake(_return_cmd=True)