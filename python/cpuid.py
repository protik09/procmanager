#!/usr/bin/env python3
"""
Handle reading the CPUID information from /sys/devices

:author: Protik Banerji <protik09@gmail.com>
"""

import os
import sys
import argparse
import coloredlogs
import logging
import subprocess
import re
import psutil

CPUINFO_LOCATION = f"/proc/cpuinfo"
CPUINFO_CURRENT_CLOCK_SPEED = []
CPUINFO_CPU_FREQ_REGEX = re.compile(r"cpu\sMHz")

def extract_full_cpu_info():
    """
    Get the information from the kernel module /proc/cpuinfo

    :author: Protik Banerji <protik09@gmail.com>
    """
    # Start logger
    func_name = sys._getframe().f_code.co_name
    eci_logger = logging.getLogger(func_name)
    eci_logger.debug("Started function " + func_name)

    # Check total number of processors on system using nproc
    eci_num_procs = subprocess.check_output('nproc')
    eci_logger.info("System has " + eci_num_procs.decode('utf-8').strip() + " logical processors.")

    # Read the CPUINFO kernel module as a file (because Linux is awesome like that)
    eci_single_proc_info = []
    eci_all_proc_info = []
    with open(CPUINFO_LOCATION) as eci:
        eci_text = eci.read().splitlines()
        print(eci_text)
        for _ in range(int(eci_num_procs)):
            line_counter = 0
            for line in eci_text:
                # Increment the line counter and break if the next processor show up
                line_counter = line_counter + 1
                if line == "":
                    break
                eci_single_proc_info.append(line)

            # Remove empty power management string from CPUinfo and strip the tabs
            eci_single_proc_info.pop(-1)
            eci_single_proc_info = [
                t.replace('\t', '') for t in eci_single_proc_info]

            # Convert the single proc info list to a dictonary and append to list of processor info
            eci_dict = dict(line.split(":") for line in eci_single_proc_info)

            # List of dicts (Dicts contain each proc info)
            eci_all_proc_info.append(eci_dict)

            # Delete the above lines from eci_text after appending into single_proc_info
            eci_single_proc_info.clear()
            for i in range(line_counter):
                eci_text.pop(i)

    # print(eci_all_proc_info)

def extract_cpu_speed_info ():
    # Start logger
    func_name = sys._getframe().f_code.co_name
    ecsi_logger = logging.getLogger(func_name)
    ecsi_logger.debug("Started function " + func_name)

    with open(CPUINFO_LOCATION) as ecsi:
        ecsi_text = ecsi.read().decode('utf-8')
        x = CPUINFO_CPU_FREQ_REGEX.findall()
        print(x)

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
