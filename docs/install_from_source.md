## Install from source

If you wish to install `crest4` from the repository source code you can follow the instructions below. This can be useful for development purposes for instance.

### Step 1: Cloning the repository

Here you will download a copy of the code from GitHub and place it in your home directory.

    $ cd ~
    $ mkdir repos
    $ cd repos
    $ git clone https://github.com/xapple/crest4.git

The read access to this repository is public.

### Step 2: Modify your python search path

Here you will edit your ``.bashrc`` or ``.bash_profile`` to add a reference to the module you just downloaded. When you type `import crest4` python will know where to look.

    $ vim ~/.bash_profile

Add this line:

    export PYTHONPATH="$HOME/repos/crest4":$PYTHONPATH

Source your bash profile to acquire these new changes:

    $ source ~/.bash_profile

### Step 3: Install your own version of python

Your system probably comes with a version of python installed, but it might be outdated or configured in a particular way. If your current version of python is at least 3.8 or above, it should be safe to skip this step.

If you are an administrator on your machine and can install the latest version of python using a package manager, you can also skip this step.

To check the version of python simply type:

    $ python3 -V

If this is not the case, and your python is outdated, we recommend installing your own python in the home directory for development purposes. Also, this guarantees that we will then be able to install python modules without administrator privileges for instance.

The easiest way to achieve this is to install miniconda by following these instructions:

https://conda.io/projects/conda/en/latest/user-guide/install/index.html

If you are using Linux this boils down to:

    $ wget https://repo.anaconda.com/miniconda/Miniconda3-py39_4.9.2-Linux-x86_64.sh
    $ bash Miniconda3-py39_4.9.2-Linux-x86_64.sh

Then you follow the interactive instructions. Once the installation is finished, you relaunch a new shell. Finally, you can create a new environment called `myenv` by typing the following command:

    $ conda create -n myenv python=3.9

To activate this environment, type:

    $ conda activate myenv

You should now be using the latest version of python.

### Step 4: Install all required python packages

`crest4` uses several extra python libraries. You can get them by running these commands:

    $ python3 -m pip install biopython
    $ python3 -m pip install ete3
    $ python3 -m pip install pytest
    $ python3 -m pip install rich
    $ python3 -m pip install setuptools
    $ python3 -m pip install autopaths
    $ python3 -m pip install optmagic
    $ python3 -m pip install plumbing
    $ python3 -m pip install seqsearch
    $ python3 -m pip install fasta

### Step 5: Obtaining extra dependencies

`crest4` makes use of two third party programs which should be installed and accessible from your ``$PATH``. These dependencies have their own specific installation procedures and include:

 * [NCBI BLAST](https://blast.ncbi.nlm.nih.gov/Blast.cgi) providing the executable ``blastn``.
 * [VSEARCH](https://github.com/torognes/vsearch) providing the executable ``vsearch``.

### Step 6: Running `crest4` without `bin/`

Since `crest4` is now installed from source, there is no executable on the `$PATH` that can be run directly.

Instead, to launch `crest4` from the command line, one must proceed as so and add a `python3 -m` suffix to each command:

    $ python3 -m crest4 -f ~/test/sequences.fasta -d silvamod138 -t 4