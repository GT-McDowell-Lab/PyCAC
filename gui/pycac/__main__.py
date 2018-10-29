'''
    Copyright 2018, Georgia Institue of Technology (C)

    This file is part of PyCAC.

    PyCAC is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    PyCAC is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with PyCAC.  If not, see <https://www.gnu.org/licenses/>.

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
