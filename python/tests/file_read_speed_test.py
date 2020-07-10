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
import platform
import mmap
# import re
# import psutil

_cpuinfo_path = f"/proc/cpuinfo"
_num_iters = 100000

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

    if int(sys.version_info[0]) == 3 and int(sys.version_info[1]) < 8:
        start = time.clock()
    else:
        start = time.time()
    for i in range(_num_iters):
        std_file_read()
    if int(sys.version_info[0]) == 3 and int(sys.version_info[1]) < 8:
        end = time.clock()
    else:
        end = time.time()
    timer = (end-start)/_num_iters
    timer = timer * 10e6
    main_logger.info(f"The stadard file read takes {timer} us")

    if int(sys.version_info[0]) == 3 and int(sys.version_info[1]) < 8:
        start = time.clock()
    else:
        start = time.time()
    for i in range(_num_iters):
        mmap_file_read()
    if int(sys.version_info[0]) == 3 and int(sys.version_info[1]) < 8:
        end = time.clock()
    else:
        end = time.time()
    timer = (end-start)/_num_iters
    timer = timer * 10e6
    main_logger.info(f"The mmap file read takes {timer} us")

