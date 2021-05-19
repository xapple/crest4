# CREST version 4.0.1

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

To produce this result, each input sequence is compared against a built-in reference database of marker genes (such as the SSU rRNA), and the exact position in the phylogenetic tree of life of every high similarity hit is recorded.

Insert brief description of the LCA method and comparison with kmers.


### Citation

If you use CREST in your research, please cite [this publication](https://dx.plos.org/10.1371/journal.pone.0049334):

    CREST - Classification Resources for Environmental Sequence Tags, PLoS ONE, 7:e49334
    Lanzén A, Jørgensen SL, Huson D, Gorfer M, Grindhaug SH, Jonassen I, Øvreås L, Urich T (2012)


## Installing

Since `crest4` is written in python it is compatible with all operating systems: Linux, macOS and Windows. The only prerequisite is `python3` which is often installed by default. Simply type one of the two following commands on your terminal, depending on which package manager you prefer to use:

    $ pip3 install crest4
    $ conda install crest4 -c conda-forge

Once the installation completes you are ready to use the `crest4` executable command from the shell. The reference databases are downloaded automatically during first run, so this might take some time depending on your internet connection.

* If you do not have `pip3` on your system you can refer to [this section](docs/installing_tips.md#obtaining-pip3).
* If you do not have `python3` on your system you can refer to [this other section](docs/installing_tips.md#obtaining-python3).
* If none the above has enabled you to install `crest4`, please open an issue on [the bug tracker](https://github.com/xapple/crest4/issues) and we will get back to you shortly.

### Database location

To download the databases that are used in the classification algorithm, `crest4` needs somewhere to write to on the filesystem. This will default to your home directory at: `~/.crest4/`. If you wish to change this, simply set the environment variable `$CREST4_DIR` to another directory path prior to execution.


## Usage

Bellow are some examples to illustrate the various ways there are to use this package.

    crest4 -f sequences.fasta

Simply specifying a FASTA file is sufficient, and `crest4` will choose default values for all the parameters automatically. The results produced will be placed in a sub-directory inside the same directory as the FASTA file. Refer to the [results](#Results) section below for more information.

To change the output directory, specify the following option:

    crest4 -f sequences.fasta -o ~/data/results/crest_test/

To parallelize the sequence similarity search with 32 processes use this option:

    crest4 -f sequences.fasta --num_threads 32

Silvamod is the default reference database. To use another database, e.g. Greengenes, the `database` option must be specified followed by the database name:

    crest4 -f sequences.fasta --search_db greengenes

### All options

The full list of options is as follows:

```
Optional arguments:

  --search_algo ALGORITHM, -a ALGORITHM
                        The algorithm used for the sequence similarity search
                        that will be run to match the sequences against the
                        database chosen. Either 'blast' or 'vsearch'. No
                        other values are currently supported. By default
                        'blast'.

  --num_threads NUM, -t NUM
                        The number of processors to use for the sequence
                        similarity search. By default parallelism is turned
                        off and this value is 1. If you pass the value `True`
                        we will run as many processes as there are CPUs but
                        no more than 32.

  --search_db DATABASE, -d DATABASE
                        The database used for the sequence similarity search.
                        Either 'silvamod128' or 'greengenes'. No other values
                        are currently supported. By default 'silvamod128'.

  --output_dir DIR, -o DIR
                        The directory into which all the classification
                        results will be written to. This defaults to a
                        directory with the same name original FASTA file and
                        a `.crest4` suffix appended.

  --search_hits PATH, -s PATH
                        The path where the search results will be stored.
                        This defaults to the output directory. However,
                        if the search operation has already been completed
                        before hand, specify the path here to skip the
                        sequence similarity search step and go directly to
                        the taxonomy step.

  --min_score MIN_SCORE, -m MIN_SCORE
                        a

  --score_drop SCORE_DROP, -c SCORE_DROP
                        a

  --version, -v         Show program's version number and exit.
  --help, -h            Show this help message and exit.

Required arguments:

  --fasta PATH, -f PATH
                        The path to a single FASTA or FASTQ file as a string.
                        These are the sequences that will be taxonomically
                        classified. The file can be gzipped or not.
```

### Python API

If you want to integrate `crest4` directly into your python pipeline, you may do so by accessing the convenient `Classify` object as follows:

    from crest4 import Classify
    tax = Classify('~/data/sequences.fasta', num_threads=16)
    output = tax()
    print(output)

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


## Results

The results produced are as follows:




## More information

### Classification databases

The SilvaMod database was derived by manual curation of the [SILVA NR SSU Ref v.128](https://www.arb-silva.de/documentation/release-128/). It supports SSU sequences from bacteria and archaea (16S) as well as eukaryotes (18S), with a high level of manual curation and defined environmental clades. Release supported: Silva NR SSU Ref v128. The database was last released in: September 2016.

The [Greengenes](http://greengenes.secondgenome.com) database is an alternative reference for classification of prokaryotic 16S, curated and maintained by The Greengenes Database Consortium. The database was last released in: May 2013

### Classification algorithm

The classification is carried out based on a subset of the best matching alignments using the [Lowest Common Ancestor](http://en.wikipedia.org/wiki/Lowest_common_ancestor) (LCA) strategy. Briefly, the subset includes sequences that score within x% of the "bit-score" of the best alignment, providing the best score is above a minimum value. Default values are `155` for the minimum bit-score and `2%` for the LCA range. Based on cross-validation testing using the non-redundant SilvaMod database, this results in relatively few false positives for most datasets. However, the LCA range can be turned up to about `10%`, to increase accuracy with short reads and for datasets with many novel sequences.

In addition to LCA classification, a minimum similarity filter is used, based on a set of taxon-specific requirements, by default depending on their taxonomic rank. By default, a sequence must be aligned with at least 99% nucleotide similarity to the best reference sequence in order to be classified to the species rank. For the genus, family, order, class and phylum ranks the respective default cut-offs are 97%, 95%, 90%, 85% and 80%. These cutoffs can be changed manually by editing the `.map` file of the respective reference database. This filter ensures that classification is made to the taxon of the lowest allowed rank, effectively re-assigning sequences to parent taxa until allowed.

When using amplicon sequences, we strongly recommend preparing the sequences by performing a noise reduction step as well as applying chimera removal. This can be achieved with various third party software: vsearch, UPARSE, DADA2, SWARM, etc.

For amplicon sequencing experiments with many replicates or similar samples (>~10), the unique noise-reduced sequences may be further clustered using a similarity threshold (often 97% although larger thresholds are probably preferable) into Operational Taxonomic Units (OTUs), prior to classification.

### Custom databases

It is possible to construct a custom reference database for use with `crest4`. The scripts necessary to do this along with some documentations are available in this other git repository:

<https://github.com/xapple/crest4_utils>

### Developer documentation

The internal documentation of the `crest4` python package is available at:

<http://xapple.github.io/crest4/crest4>

This documentation is simply generated from the source code with this command:

    $ pdoc3 --html --output-dir docs --force crest4
