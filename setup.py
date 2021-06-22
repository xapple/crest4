#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Imports #
from setuptools import setup, find_namespace_packages
from os import path

# Load the contents of the README.md file #
this_dir = path.abspath(path.dirname(__file__))
readme_path = path.join(this_dir, 'README.md')
with open(readme_path, encoding='utf-8') as handle: readme = handle.read()

# Call setup #
setup(
    name             = 'crest4',
    version          = '4.0.15',
    description      = 'The `crest4` python package can automatically assign '
                       'taxonomic names to DNA sequences obtained from '
                       'environmental sequencing.',
    license          = 'GPL3',
    url              = 'https://github.com/xapple/crest4/',
    author           = 'Anders Lanzén and Lucas Sinclair',
    author_email     = 'anders.lanzen@gmail.com',
    classifiers      = ['Topic :: Scientific/Engineering :: Bio-Informatics'],
    packages         = find_namespace_packages(),
    install_requires = ['autopaths>=1.5.0', 'optmagic>=1.0.8',
                        'plumbing>=2.10.4', 'fasta>=2.2.11',
                        'seqsearch>=2.1.2', 'biopython', 'rich', 'ete3',
                        'pytest'],
    python_requires  = ">=3.8",
    entry_points     = {"console_scripts": ["crest4 = crest4.__main__:main"]},
    long_description = readme,
    long_description_content_type = 'text/markdown',
    include_package_data = True,
)