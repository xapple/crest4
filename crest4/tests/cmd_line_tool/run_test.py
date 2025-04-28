#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Script to run the `cmd_line_tool` integration test.
"""

# Built-in modules #
import inspect, sys, subprocess

# First party modules #
from autopaths import Path

# Third party modules #
import pytest, asyncio

# Internal modules #

# Get the current directory of this python script #
this_file = Path((inspect.stack()[0])[1])
this_dir  = this_file.directory

###############################################################################
@pytest.mark.asyncio
async def test_cmd_line_tool():
    # The input fasta #
    fasta = this_dir.find('*.fasta')
    # The output directory #
    output_dir = this_dir + 'results/'
    output_dir.remove()
    # Build the command as a list of arguments
    cmd = [sys.executable,
           '-m', 'crest4',
           '--fasta', fasta,
           '--output_dir', output_dir,
           '--num_threads', 'True']
    # Run the command asynchronously
    process = await asyncio.create_subprocess_exec(*cmd,
                                                   stdout = subprocess.PIPE,
                                                   stderr = subprocess.PIPE)
    # Wait for the process to finish #
    stdout, stderr = await process.communicate()
    # Check that the results were created #
    created_file = output_dir + 'assignments.txt'
    assert created_file
    # Check that the return code is 0 #
    assert process.returncode == 0
    # Return #
    return process

###############################################################################
if __name__ == '__main__':
    process = test_cmd_line_tool()
    asyncio.run(process)
