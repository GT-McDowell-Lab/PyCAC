#!/usr/bin/env python
#title:cacClass.py
#description:CAC object to facilitate parametric study definition
#					
#author:chu.k@gatech.edu
#updated:2018/07/02
#version:0.3
#usage:N/A
#notes:McDowell Lab PyCAC. Version req for dictionary order preservation
#python_version:3.6.4
#==============================================================================
from .InputClass import CommandList
import glob
import copy, os
import shutil
from os.path import realpath, split, isfile, join


class Cac: 
	# CAC simulation interface
	def __init__(self, base_input=CommandList()):
		# deep copy of CommandList object
		self.description = "RUN"

		self.input = copy.deepcopy(base_input)

		self.restart_data_files = ""

		self.output_dir = ""

		self.potential_files = ""

		self.add_atom_data_files = ""

	def set_restart(self, path_list):
		# Define the restart directory to search for restart file
		if self.input.restart['boolean_restart'] == 't':				
			files = (self.__check_restart(path_list))
			if files:
				self.restart_data_files = files
				return True
			return False
		else:
			return True
	
	def set_restart_exists(self, path):
		if self.input.restart['boolean_restart'] == 't':
			restart_file = [join(path, r) for r in glob.glob1(path, "cac_in.restart")]
			print(restart_file)
			if not restart_file:
				return(1, "Restart mode specified, but cac_in.restart is missing from run directory.")
			group_files = [join(path, g) for g in glob.glob1(path, "group_in_*.id")]
			print(group_files)
			expected = int(self.input.group_num['restart_group_number'])
			if len(group_files) != expected:
				return(1, "({}) group files found, but {} are expected".format(len(group_files), expected))
			self.restart_data_files = restart_file + group_files
			return(0, "Passed basic checks")
		else:
			return (0, 0)

	def set_potential(self, directory):
		files = self.__check_potential(directory)
		if files:
			self.potential_files = [realpath(file) for file in files]
			return True
		else:
			return False

	def set_output(self, directory):
		if not directory:
			self.input.errors.append(('output', "Output directory was not provided"))
			return False
		self.output_dir = directory
	
	def set_add_atoms(self, lmp_files):
		if lmp_files:
			new_files = self.__check_add_atoms(lmp_files)
			if not new_files:
				self.input.errors.append(('modify', "Failed to copy necessary add_atom LAMMPS files"))
				return False
			self.add_atom_data_files = new_files
			return True
		else:
			return True

	def __check_restart(self, path_list):
		if not path_list[0]:
			self.input.errors.append(('Restart', "Restart path was not provided"))
			return False
		print(path_list)
		# Grab the restart file first
		basename, file = split(path_list[0])
		groups = path_list[1]
		refine_order = path_list[2]

		if file == "cac_in.restart":
			self.input.errors.append(('restart', "Please select a restart file in the unchanged output format: cac_out_#.restart"))
			return False
		# Make a copy, rename
		copy_handler(path_list[0], join(basename, "cac_in.restart"))
		files = [join(basename, "cac_in.restart")]

		timestep = file.split('_')[-1].split('.')[0]
		print(timestep)
		# No group files
		if not groups:
			return files

		# rearrange the groups list according to refine order
		reordered_groups = []
		[reordered_groups.append(groups[f]) for f in refine_order]
		for i, group in enumerate(groups):
			if i not in refine_order:
				reordered_groups.append(group)

		print(groups, reordered_groups)

		# For each file in the enum() path list (except restart)
		new_groups = self.input.group_num['new_group_number']
		for i, group in enumerate(reordered_groups):
			print(group)
		# 	redundancy check that it exists
			if not isfile(group):
				err_stat = ("Restart group file not found ({}).".format(group))
				self.input.errors.append(('restart', err_stat))
				return False
			curr_t = group.split('_')[-1].split('.')[0]
			print(curr_t)
		#	check the timestep matches up; append error if not
			if int(curr_t) != int(timestep):
				err_stat = ("Output group file specified does not match the timestep of the restart file ({}).".format(timestep))
				self.input.errors.append(('restart', err_stat))
				return False
		#	rename as group_in_i.id
			input_group = join(basename, "group_in_{}.id".format(i+1+new_groups))
			copy_handler(group, input_group)
			files.append(input_group)

		print(files)
		return files

	def __check_potential(self, dir):
		# See if the potential file exists in the path
		success = True
		if not dir:
			self.input.errors.append(('Potential', "Potential path was not provided"))
			return False
		potential_exists = False
		typef = self.get_parameter('potential', 'potential_type')
		if typef == 'eam':
			expected = ['edens.tab', 'embed.tab', 'pair.tab']
			potential_exists = [join(dir, tab) for tab in (glob.glob1(dir,'*.tab'))]

			if len(potential_exists) < 3:
				err_stat = "3 .tab files are required for an EAM potential"
				self.input.errors.append(('potential', err_stat))
			# Downloaded directory will have potential_distance.tab from CAC output
			elif len(potential_exists) > 3:
				[potential_exists.remove(item) for item in potential_exists if item not in expected]

		elif typef == 'lj':
			potential_exists = [join(dir, para) for para in (glob.glob1(dir, 'lj.para'))]

		if not potential_exists:
			err_stat = ("({}) Potential files not found on path ({})".format(typef, dir))
			self.input.errors.append(('potential', err_stat))
			return False

		return potential_exists

	def __check_add_atoms(self, lmp_files):
		new_files = []
		for n, dat in lmp_files:
			# Copy and rename in place for easy access
			if isfile(dat):
				err, val = check_dat(dat)
				if err:
					self.input.errors.append(('modify', val))
					return False
				basename, file = split(dat)
				new_name = join(basename, 'lmp_{}.dat'.format(n))
				print("\t Copy {} >> {}".format(dat, new_name))
				copy_handler(dat, new_name)
				new_files.append(new_name)
			else:
				return False
		return new_files

	def edit_command(self, command_name, parameter_list):
		try:
			self.input.edit_command(command_name, parameter_list)
			return
		except IndexError:
			err_stat = ("No. of parameters provided to ({}) are incorrect ".format(command_name))
			self.input.errors.append((command_name, err_stat))
			return

	def edit_parameter(self, command_name, parameters, value):
		if isinstance(parameters, list):
			err_stat = self.input.edit_parameter(command_name, parameters, value)
		else:
			err_stat = self.input.edit_parameter(command_name, [parameters], value)
		if err_stat:
			return self.input.errors.append((command_name, err_stat[1]))
		else:
			return True

	def get_parameter(self, command_name, parameters):
		if isinstance(parameters, list):
			return self.input.get_parameter(command_name, parameters)
		else:
			return self.input.get_parameter(command_name, [parameters])


	def get_command(self, command_name):
		# Mostly for debugging purposes. 
		return (self.input.parse_command(command_name))

	def get_errors(self):
		return(len(self.input.errors), self.input.errors)

	def check_dependencies(self):

		# definied grain_num must match grain_mat input 
		grain_n_def = self.get_parameter('grain_num', 'grain_number')
		grain_n_in = len(self.input.grain_mat.keys())
		if  grain_n_def != grain_n_in:
			self.input.errors.append(('grain_num', "({}) grain(s) defined in grain_num, found ({}) in grain_mat".format(grain_n_def, grain_n_in)))
		# subdomain, unit_num, unit_type dependencies are checked in uploads.py
		# (function: convert_vals)

		# modify_num must match modifies
		mod_n_def = self.get_parameter('modify_num', 'modify_number')
		mod_n_in = len(self.input.modify.keys())
		if  mod_n_def != mod_n_in:
			self.input.errors.append(('modify_num', "({}) modify(s) defined in modify_num, found ({}) in input script".format(mod_n_def, mod_n_in)))
		# New groups
		group_n_def = self.get_parameter('group_num', 'new_group_number')
		group_n_in = len(self.input.group.keys())
		if  group_n_def != group_n_in:
			self.input.errors.append(('group_num', "({}) new groups(s) defined in group_num, found ({}) in input script".format(group_n_def, group_n_in)))
		# Fixes
		fix_n_def = self.get_parameter('group_num', 'fix_number')
		fix_n_in = len(self.input.fix.keys())
		if  fix_n_def != fix_n_in:
			self.input.errors.append(('group_num', "({}) fix(es) defined in group_num, found ({}) in input script".format(fix_n_def, fix_n_in)))
		# Cals
		cal_n_def = self.get_parameter('group_num', 'cal_number')
		cal_n_in = len(self.input.cal.keys())
		if  cal_n_def != cal_n_in:
			self.input.errors.append(('group_num', "({}) cal(s) defined in group_num, found ({}) in input script".format(cal_n_def, cal_n_in)))

# Util
def copy_handler(src, dst):
	try:
		shutil.copy(src, dst)
		return dst
	except shutil.SameFileError:
		if src == dst:
			pass
			return dst
		os.remove(src)
		shutil.copy(src, dst)
		return dst

def check_dat(filename):
	with open(filename, 'r') as dat_fp:
		for i, line in enumerate(dat_fp):
			print(line)
			try:
				if i == 2:
					n_atom, text = line.split()
					if text != 'atom':
						return((1, "Invalid format of dat file"))
				elif i == 11:
					vals = line.split()
					if len(vals) != 5:
						return((1, "Invalid format of dat file"))
			except ValueError:
				return((1, "Invalid format of dat file"))
	return(0, "Passed checks")
