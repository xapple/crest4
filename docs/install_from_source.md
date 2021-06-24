## Install from source

If you wish to install `crest4` from the repository source code you can follow the instructions below. This can be useful for development purposes for instance.

### Step 1: Cloning the repository

Here you will download a copy of the code from github and place it in your home directory.

    $ cd ~
    $ mkdir repos
    $ cd repos
    $ git@github.com:xapple/crest4.git

The read access to this repository is public.

### Step 2: Modify your python search path

Here you will edit your ``.bashrc`` or ``.bash_profile`` to add a reference to the module you just downloaded. When you type `import crest4` python will know where to look.

    $ vim ~/.bash_profile

Add this line:

    export PYTHONPATH="$HOME/repos/crest4":$PYTHONPATH

### Step 3: Install your own version of python

Your system probably comes with a version of python installed. But the variations from system to system are too great to rely on any available setup. We recommend to install our own in the home directory for development purposes. Also, we will then be able to install modules without administrator privileges. You can skip this step if you are confident enough about about your system's python or are an administrator.

For this we will be using this excellent project: https://github.com/yyuu/pyenv

To install it you may use this sister project: https://github.com/yyuu/pyenv-installer

Basically you just need to type this command:

    $ curl https://pyenv.run | bash

These lines go into your ``.bash_profile``:

    export PATH="$HOME/.pyenv/bin:$PATH"
    eval "$(pyenv init -)"
    eval "$(pyenv virtualenv-init -)"

Relaunch your shell and type these commands to get the right version of python:

    $ pyenv install 3.9.5
    $ pyenv global 3.9.5
    $ pyenv rehash

### Step 4: Install all required python packages

`crest4` uses several extra python libraries. You can get them by running these commands:

    $ python3 -m pip install biopython
    $ python3 -m pip install ete3
    $ python3 -m pip install pytest
    $ python3 -m pip install rich
    $ python3 -m pip install autopaths
    $ python3 -m pip install optmagic
    $ python3 -m pip install plumbing
    $ python3 -m pip install seqsearch
    $ python3 -m pip install fasta

### Step 5: Obtaining extra dependencies

`crest4` makes use of two third party programs which should be installed and accessible from your ``$PATH``. These dependencies have their own specific installation procedures and include:

 * [NCBI BLAST](https://blast.ncbi.nlm.nih.gov/Blast.cgi) providing the executable ``blastn``.
 * [VSEARCH](https://github.com/torognes/vsearch) providing the executable ``vsearch``.