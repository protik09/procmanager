#!/usr/bin/env python3
"""
Handle reading the CPUID information from psutil

:author: Protik Banerji <protik09@gmail.com>
"""

import os
import sys
import psutil
import logging
import coloredlogs


# Main program for testing purposes only

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

    main_logger.debug("Welcome to the CPUID program module.")
    # extract_full_cpu_info()
    # psutil.cpu_count()
    extract_cpu_speed_info()
