#!/usr/bin/env python3
"""
Test the various methods of file reads to benchmark the ones for lowest overhead.

:author: Protik Banerji <protik09@gmail.com>
"""

import os
import sys
import argparse
import coloredlogs
import logging
import time
# import re
# import psutil

_cpuinfo_path = f"/proc/cpuinfo"

def std_file_read():
    """
    Benchmark standard file read in python in WSL and Native Linux
    """
    with open(_cpuinfo_path) as f:
        x = f.read()

def mmap_file_read():
    """
    Benchmark mmap file read in python in WSL and Native Linux
    """
    with open(_cpuinfo_path) as f:
        mm = mmap.mmap(f.fileno(), 0)
        x = mm.read()


if __name__ == "__main__":
    main_logger = logging.getLogger(__name__)

    # Argument parsing section
    parser = argparse.ArgumentParser()
    parser.add_argument('--debug', action='store_true',
                        help='Activate debug outputs when active.')
    args = parser.parse_args()

    if args.debug:
        coloredlogs.install(level='DEBUG')
    else:
        coloredlogs.install(level='INFO')

    main_logger.info("Welcome to the File Read test program module.")

    start = time.clock()
    for i in range(1000):
        function()
    end = time.clock()
    time = (end-start)/1000
    main_logger.info(f"The stadard file read takes {time} s")

    start = time.clock()
    for i in range(1000):
        function()
    end = time.clock()
    time = (end-start)/1000
    main_logger.info(f"The stadard file read takes {time} s")
