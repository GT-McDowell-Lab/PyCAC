#!/usr/bin/env python

'''
Implementation of the script usage
The main function takes one argument:
functionality: --config(-c) or --job(-j)

'''
import os
import sys
import json
import argparse

# Using python defined argument parser
parser = argparse.ArgumentParser(description = 'Deploy CAC to the cluster, or create/batch submit jobs to the cluster')
#parser.add_argument('functionality', help = 'Actions that can be done. Actions are: train (t), visualize (v)')

parser.add_argument('-c', '--configure', help = 'Configure CAC on cluster', action='store_true')
parser.add_argument('-j', '--job', help = 'Create, submit, and download PyCAC jobs', action='store_true')


# If you need more argument(s), change the following line into what you need or add
# another line if you need more than 2 arguments
'''
parser.add_argument('-v', # name for the argument
                    '--variable', # long name for the argument
                    dest = 'variable', # the name you use for accessing the variable from args
                    help = 'set up an arbitrary variable', # help message when type in -h for help
                    default = 5, # defualt value is set to 5
                    type = int)
'''

if len(sys.argv[1:])==0:
    parser.print_help()
    parser.exit()

args = parser.parse_args()

if args.job:
    from .MainWindow import start_job_gui
    start_job_gui()
    
elif args.configure:
    from .SetupWindow import start_config_gui
    start_config_gui()
