#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Written by Lucas Sinclair.
GNUv3 Licensed.
Contact at www.sinclair.bio
Created in May 2021.
"""

# Imports #
from setuptools import setup, find_namespace_packages
from os import path

# Load the contents of the README file #
this_dir = path.abspath(path.dirname(__file__))
readme_path = path.join(this_dir, 'README.md')
with open(readme_path, encoding='utf-8') as handle: readme = handle.read()

# Call setup #
setup(
    name             = 'crest4',
    version          = '4.0.10',
    description      = 'The `crest4` python package can automatically assign '
                       'taxonomic names to DNA sequences obtained from '
                       'environmental sequencing.',
    license          = 'GPL3',
    url              = 'https://github.com/xapple/crest4/',
    author           = 'Anders Lanzen and Lucas Sinclair',
    author_email     = 'anders.lanzen@gmail.com',
    classifiers      = ['Topic :: Scientific/Engineering :: Bio-Informatics'],
    packages         = find_namespace_packages(),
    install_requires = ['plumbing>=2.9.10', 'fasta>=2.2.6',
                        'seqsearch>=2.0.2', 'autopaths>=1.4.8',
                        'optmagic>=1.0.4', 'biopython', 'rich',
                        'ete3', 'pytest'],
    python_requires  = ">=3.6",
    entry_points     = {"console_scripts": ["crest4 = crest4.__main__:main"]},
    long_description = readme,
    long_description_content_type = 'text/markdown',
    include_package_data = True,
)