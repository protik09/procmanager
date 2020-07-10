#!/usr/bin/env python3
"""
Handle reading the CPUID information from psutil

:author: Protik Banerji <protik09@gmail.com>
"""

import os
import platform
import sys
import subprocess
import argparse
import psutil
import logging
import coloredlogs
import re

# Define some globals here
CPU_BASE_FREQUENCY = 0.0
CPU_MAX_CURRENT_FREQUENCY = 0.0 # This shows the value of the core with the highest clock
CPU_AVG_UTIL = 0.0 # Average load across all cores
CPU_NUM_SOCKET = 0
CPU_NUM_PHY_CORES = 0
CPU_NUM_LOG_CORES = 0
CPU_VIRT_FLAG = None
CPU_L1_CACHE = 0.0
CPU_L2_CACHE = 0.0
CPU_L3_CACHE = 0.0
CPU_UPTIME = None
CPU_NAME = ""
CPUINFO_LOCATION = f"/proc/cpuinfo"


def get_processor_name():
    """
    Hacky console code to get processor name.

    :source: https://stackoverflow.com/questions/4842448/getting-processor-information-in-python
    """
    # Start logger
    func_name = sys._getframe().f_code.co_name
    gpn_logger = logging.getLogger(func_name)
    gpn_logger.debug("Started function " + func_name)

    if platform.system() == "Windows":
        return platform.processor()

    elif platform.system() == "Darwin":
        os.environ['PATH'] = os.environ['PATH'] + os.pathsep + '/usr/sbin'
        command = "sysctl -n machdep.cpu.brand_string"
        return subprocess.check_output(command).strip()

    elif platform.system() == "Linux":
        gpn_logger.debug(f"Detected {platform.system()}")
        with open(CPUINFO_LOCATION) as eci:
            eci_text = eci.read().splitlines()
        print()
        for line in eci_text:
            gpn_logger.debug(line)
            if "model name" in line:
                print()
                gpn_logger.debug("Found model name\n")
                return re.sub(".*model name.*:", "", str(line), 1)

        # If the model name is not found spit out a warning
        gpn_logger.error("\nCPU Model name not found")

    return ""

def static_cpu_info():
    """
    Grab CPU stats that don't change with time.
    """
    global CPU_NAME
    CPU_NAME = get_processor_name()


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

    main_logger.info("Welcome to the CPUID program module.")

    # Check if running on Linux and only Linux for now
    if psutil.LINUX:
        static_cpu_info()
        # Print the static CPU Info
        print(f"CPU Name: {CPU_NAME}")
        # extract_full_cpu_info()
        # psutil.cpu_count()
        # extract_cpu_speed_info()
    else:
        main_logger.error("Please run this program only in Linux. Exiting.....")

