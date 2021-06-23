[![PyPI version](https://badge.fury.io/py/crest4.svg)](https://badge.fury.io/py/crest4)
![Pytest passing](https://github.com/xapple/crest4/actions/workflows/pytest_master_branch.yml/badge.svg)

# CREST version 4.0.25

`crest4` is a python package for automatically assigning taxonomic names to DNA sequences obtained from environmental sequencing.

<p align="center">
<img height="143" src="docs/logo.png?raw=true" alt="CREST Logo">
</p>

More specifically, the acronym CREST stands for "Classification Resources for Environmental Sequence Tags" and is a collection of software and databases for taxonomic classification of environmental marker genes obtained from community sequencing studies. Such studies are also known as "meta-genomics", "meta-transcriptomics", "meta-barcoding", "taxonomic profiling" or "phylogenetic profiling".

Simply put, given the following fragment of an rRNA 16S sequence from an uncultured microbe:

    TGGGGAATTTTCCGCAATGGGCGAAAGCCTGACGGAGCAATACCGCGTGAGGGAGGAAGGCCTTAGGGTT
    GTAAACCTCTTTTCTCTGGGAAGAAGATCTGACGGTACCAGAGGAATAAGCCTCGGCTAACTCCGTGCCA
    GCAGCCGCGGTAAGACGGAGGAGGCAAGCGTTATCCGGAATTATTGGGCGTAAAGCGTCCGTAGGCGGTT
    AATTAAGTCTGTTGTTAAAGCCCACAGCTCAACTGTGGATCGGCAATGGAAACTGGTTGACTAGAGTGTG
    GTAGGGGTAGAGGGAATTCCCGGTGTAGCGGTGAAATGCGTAGATATCG

`crest4` will be able to tell you that this gene is likely originating from the following taxonomy order:

    Bacteria; Terrabacteria; Cyanobacteria; Oxyphotobacteria; Synechococcales

To produce this result, the input sequence is compared against a built-in reference database of marker genes (such as the SSU rRNA), using the BLAST or VSEARCH algorithms. All high similarity hits are recorded and filtered for both a minimum score threshold, and a minimum identify threshold. Next, for every surviving hit, the exact position in the phylogenetic tree of life is recorded. Finally, the full name of the lowest common ancestor (given this collection of nodes in the tree) is determined and reported as a confident taxonomic classification.

This strategy contrasts with the other tools that instead use a naive bayesian classifier for taxonomic assignment. Often referred to as the Wang method and used for instance in the RDP software, it consists of the following steps: calculate the probability that the query sequence would be part of any given reference taxonomy sequence based on the decomposed *kmer* content and pick the taxonomy with the highest probability while considering a confidence limit computed by a bootstrapping algorithm.

### Citation

If you use CREST in your research, please cite [this publication](https://dx.plos.org/10.1371/journal.pone.0049334):

    CREST - Classification Resources for Environmental Sequence Tags, PLoS ONE, 7:e49334
    Lanzén A, Jørgensen SL, Huson D, Gorfer M, Grindhaug SH, Jonassen I, Øvreås L, Urich T (2012)


## Installing

Since `crest4` is written in python it is compatible with all operating systems: Linux, macOS and Windows. The only prerequisite is python version 3.8 or above which is often installed by default. Simply choose one of the two following methods, depending on which package manager you prefer to use.

### Installing via `conda`

    $ conda install -c bioconda -c conda-forge -c xapple crest4 

### Installing via `pip`

    $ pip3 install crest4

### Notes and extras

Once the installation completes you are ready to use the `crest4` executable command from the shell. Please note that the reference databases are downloaded automatically during first run, so this might take some time depending on your internet connection.

In order to search the reference databases, you will also need either BLAST or VSEARCH installed. These are installed automatically with the `conda` method, but not with the `pip` method. You can obtain these with these commands on Linux:

    $ sudo apt install ncbi-blast+
    $ sudo apt install vsearch

Or these commands on macOS:

    $ brew install blast
    $ brew install vsearch

### Troubleshooting

* If you do not have `pip3` on your system you can refer to [this section](docs/installing_tips.md#obtaining-pip3).
* If you do not have `python3` on your system or have an outdated version, you can refer to [this other section](docs/installing_tips.md#obtaining-python3).
* If you can't run the `crest4` command after a successful installation, make sure that the python bin directory is in your path. This is usually `$HOME/.local/bin/` for Ubuntu.
* If none of the above has enabled you to install `crest4`, please open an issue on [the bug tracker](https://github.com/xapple/crest4/issues) and we will get back to you shortly.

### Database location

To download the databases that are used in the classification algorithm, `crest4` needs somewhere to write to on the filesystem. This will default to your home directory at: `~/.crest4/`. If you wish to change this, simply set the environment variable `$CREST4_DIR` to another directory path prior to execution.

## Usage

Bellow are some examples to illustrate the various ways there are to use this package.

    crest4 -f sequences.fasta

Simply specifying a FASTA file with the sequences to classify is sufficient, and `crest4` will choose default values for all the parameters automatically. The results produced will be placed in a sub-directory inside the same directory as the FASTA file.

To change the output directory, specify the following option:

    crest4 -f sequences.fasta -o ~/data/results/crest_test/

To parallelize the sequence similarity search with 32 threads use this option:

    crest4 -f sequences.fasta -t 32

Silvamod128 is the default reference database. To use another database, e.g. Greengenes, the `d` option must be specified followed by the database name:

    crest4 -f sequences.fasta -d greengenes

### All options

The full list of options is as follows:

```
Required arguments:
  --fasta PATH, -f PATH
                        The path to a single FASTA file as a string.
                        These are the sequences that will be taxonomically
                        classified.

Optional arguments:
  --search_algo ALGORITHM, -a ALGORITHM
                        The algorithm used for the sequence similarity search
                        that will be run to match the sequences against the
                        database chosen. Either `blast` or `vsearch`. No
                        other values are currently supported. By default
                        `blast`.

  --num_threads NUM, -t NUM
                        The number of processors to use for the sequence
                        similarity search. By default parallelism is turned
                        off and this value is 1. If you pass the value `True`
                        we will run as many processes as there are CPUs but
                        no more than 32.

  --search_db DATABASE, -d DATABASE
                        The database used for the sequence similarity search.
                        Either `silvamod128` or `greengenes`. No other values
                        are currently supported. By default `silvamod128`.

  --output_dir DIR, -o DIR
                        The directory into which all the classification
                        results will be written to. This defaults to a
                        directory with the same name as the original FASTA
                        file and a `.crest4` suffix appended.

  --search_hits PATH, -s PATH
                        The path where the search results will be stored.
                        This defaults to the output directory. However,
                        if the search operation has already been completed
                        before hand, specify the path here to skip the
                        sequence similarity search step and go directly to
                        the taxonomy step.

  --min_score MINIMUM, -m MINIMUM
                        The minimum bit-score for a search hit to be considered
                        when using BLAST as the search algorithm. All hits below
                        this score are ignored. When using VSEARCH, this value
                        instead indicates the minimum identity between two
                        sequences for the hit to be considered.
                        The default is `155` for BLAST and `0.75` for VSEARCH.

  --score_drop SCORE_DROP, -c SCORE_DROP
                        Determines the range of hits to retain and the range
                        to discard based on a drop in percentage from the score
                        of the best hit. Any hit below the following value:
                        "(100 - score_drop)/100 * best_hit_score" is ignored.
                        By default `2.0`.

  --min_smlrty MIN_SMLRTY, -i MIN_SMLRTY
                        Determines if the minimum similarity filter is turned
                        on or off. Pass the value `False` to turn it off.
                        The minimum similarity filter prevents classification
                        to higher ranks when a minimum rank-identity is not met.
                        By default `True`.

Other arguments:
  --version, -v         Show program's version number and exit.
  --help, -h            Show this help message and exit.
  --pytest              Run the test suite and exit.
```

### Python API

If you want to integrate `crest4` directly into your python pipeline, you may do so by accessing the convenient `Classify` object as follows:

    # Import #
    from crest4 import Classify
    # Create a new instance #
    get_tax = Classify('~/data/sequences.fasta', num_threads=16)
    # Run the simliarty search and classification #
    get_tax()
    # Print the results #
    for name, query in get_tax.queries_by_id.items():
        print(name, query.taxonomy)

The specific arguments accepted are the same as the command line version as specified in the [internal API documentation](http://xapple.github.io/crest4/crest4/classify#Classify).

### Test suite

To test that the installation was successful you can launch the test suite by executing:

    crest4 --pytest

### Splitting computation

It is possible to run the sequence similarity search yourself without passing through the `crest4` executable. This is useful for instance if you want to run BLAST on a dedicated server for increased speed and only want to perform the taxonomic assignment on your local computer.

In such a case you just need to copy the hits file that was generated back to your local computer and specify its location with the following parameter:

    crest4 sequences.fasta --hits_file=~/results/seq_search.hits

To create the hits file on a different server you should call the `blastn` executable with the following options:

    blastn -query sequences.fasta -db ~/.crest4/silvamod128/silvamod128.fasta -num_alignments 100 -outfmt "7 qseqid sseqid bitscore length nident" -out seq_search.hits

We also recommend that you use `-num_threads` to enable multi-threading and speed up the alignments.

The equivalent VSEARCH command is the following:

    vsearch --usearch_global sequences.fasta -db ~/.crest4/silvamod128/silvamod128.udb -blast6out seq_search.hits -threads 32 -id 0.75 -maxaccepts 100


## More information

### Classification databases

The `silvamod128` database was derived by manual curation of the [SILVA NR SSU Ref v.128](https://www.arb-silva.de/documentation/release-128/). It supports SSU sequences from bacteria and archaea (16S) as well as eukaryotes (18S), with a high level of manual curation and defined environmental clades. Release supported: Silva NR SSU Ref v128. This database was last released in September 2016.

The [Greengenes](http://greengenes.secondgenome.com) database is an alternative reference for classification of prokaryotic 16S, curated and maintained by The Greengenes Database Consortium. This database was last released in May 2013.

### Classification algorithm

The classification is carried out based on a subset of the best matching alignments using the [Lowest Common Ancestor](http://en.wikipedia.org/wiki/Lowest_common_ancestor) strategy. Briefly, the subset includes sequences that score within x% of the "bit-score" of the best alignment, provided the best score is above a minimum value. Default values are `155` for the minimum bit-score and `2%` for the score drop threshold. Based on cross-validation testing using the non-redundant Silvamod128 database, this results in relatively few false positives for most datasets. However, the score drop range can be turned up to about `10%`, to increase accuracy with short reads and for datasets with many novel sequences.

In addition to the lowest common ancestor classification, a minimum similarity filter is used, based on a set of taxon-specific requirements, by default depending on their taxonomic rank. By default, a sequence must be aligned with at least 99% nucleotide similarity to the best reference sequence in order to be classified to the species rank. For the genus, family, order, class and phylum ranks the respective default cut-offs are 97%, 95%, 90%, 85% and 80%. These cutoffs can be changed manually by editing the `.map` file of the respective reference database. This filter ensures that classification is made to the taxon of the lowest allowed rank, effectively re-assigning sequences to parent taxa until allowed.

When using amplicon sequences, we strongly recommend preparing the sequences by performing a noise reduction step as well as applying chimera removal. This can be achieved with various third party software such as: VSEARCH, UPARSE, DADA2, SWARM, etc.

For amplicon sequencing experiments with many replicates or similar samples (>~10), the unique noise-reduced sequences may be further clustered using a similarity threshold (often 97% although larger thresholds are probably preferable) into operational taxonomic units (OTUs), prior to classification.

### Custom databases

It is possible to construct a custom reference database for use with `crest4`. The scripts necessary to do this along with some documentations are available in this other git repository:

<https://github.com/xapple/crest4_utils>

### QIIME2 plug-in

A plug-in for usage with QIIME2 is being developed and will be accessible here once completed:

<https://github.com/xapple/q2-crest4>

### Continuous testing

The repository for `crest4` comes along with five different GitHub actions for CI/CD which are:

* Pytest master branch
* Test PyPI release on Ubuntu ![Pytest passing](https://github.com/xapple/crest4/actions/workflows/test_pypi_ubuntu.yml/badge.svg)
* Test PyPI release on macOS ![Pytest passing](https://github.com/xapple/crest4/actions/workflows/test_pypi_macos.yml/badge.svg)
* Test conda release on Ubuntu ![Pytest passing](https://github.com/xapple/crest4/actions/workflows/test_conda_ubuntu.yml/badge.svg)
* Test conda release on macOS ![Pytest passing](https://github.com/xapple/crest4/actions/workflows/test_conda_macos.yml/badge.svg)

Only the first action is set to be run automatically on each commit to the master branch. The four other actions can be manually launched and will run the pytest suite for both python 3.8 and python 3.9 on different operating systems.

### Developer documentation

The internal documentation of the `crest4` python package is available at:

<http://xapple.github.io/crest4/crest4>

This documentation is simply generated from the source code with this command:

    $ pdoc3 --html --output-dir docs --force crest4
