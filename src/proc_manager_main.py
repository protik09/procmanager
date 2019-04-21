#!/usr/bin/env python3
"""
Main process for open source task manager for Linux and Windows

:author: Protik Banerji <protik09@gmail.com>
"""

import argparse
import coloredlogs
import logging
import os
import sys
import multiprocessing as mp
import numpy as np
import traceback

import third_party_libs.cpu_info as ci

def ProcManagerMain(debug_flag, info_flag):
	# Install loggers if flags passed
	if debug_flag:
		coloredlogs.install("DEBUG")
	elif debug_flag:
		coloredlogs.install("INFO")
	else:
		pass

	# Start the logger by getting the current function name using this pseudo-macro function
	pmm_logger = logging.getLogger(sys._getframe().f_code.co_name)


if __name__ == "__main__":
	# Start all the loggers!!
	main_logger = logging.getLogger(__name__)

	# Argument parsing section
	parser = argparse.ArgumentParser()
	parser.add_argument('--debug', action='store_true',
						help='Activate debug outputs when active.')
	parser.add_argument('--info', action='store_true',
						help='Activate info outputs when active.')
	args = parser.parse_args()
	try:
		ProcManagerMain(args.debug, args.info)
	except Exception as e:
		traceback.print_exc(e)
