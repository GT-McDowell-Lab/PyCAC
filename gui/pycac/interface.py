#!/usr/bin/env python
#title:interface.py
#description:Job directory setup and cluster interfacing main handler
#			
#author:chu.k@gatech.edu
#updated:2018/07/02
#version:0.2
#usage:N/A
#notes:McDowell Lab PyCAC. Version req for dictionary order preservation
#python_version:3.6.4
#==============================================================================
from .InputClass import CommandList, unit, rotated_bases
from .CacClass import Cac, copy_handler
from .ssh_util import upload, login
from re import split
import os, sys
import glob
import shutil
import datetime
import tarfile
import time
import json
import errno
import pycac

def create_base_input(input_vals, config_vals, add_atom_vals):
	'''
	Generate single Cac object from input, validate fields
	input_vals = [(cmd1, parameters1[]), (cmd2, parameters[])]
	config_vals = [restart_file, output_dir, potential_path]
	TODO: add_atom_vals = [(id1, lmp_dat1), (id2, lmp_dat2)]
	'''
	# Populate the base class with all input args
	base_cac = Cac()
	# Edit command list
	# swap group_num to the front
	for i, tup in enumerate(input_vals):
		cmd, param = tup
		if cmd == 'group_num':
			g = i
			break
	input_vals[g], input_vals[0] = input_vals[0], input_vals[g]

	for cmd, params in input_vals:
		print(cmd, params)
		base_cac.edit_command(cmd, params)

	print(config_vals)
	base_cac.set_output(os.path.realpath(config_vals[1]))
	base_cac.set_potential(os.path.realpath(config_vals[2]))
	base_cac.set_add_atoms(add_atom_vals)
	base_cac.set_restart(config_vals[0])

	all_commands = vars(base_cac.input).keys() 
	command_string_list = []
	# Parse each command dict
	for command in all_commands:
		command_string_list.append(base_cac.input.parse_command(command))

	return base_cac

def last_edited(instance_dict):
	# Get the most recent set of simulation instances to squelch repetition
	most_recent_list = []
	for cmd in instance_dict:
		if cmd != 'base':
			for prm in instance_dict[cmd]:
				if len(instance_dict[cmd][prm]) > len(most_recent_list):
					most_recent_list = instance_dict[cmd][prm]
	if not most_recent_list:
		return instance_dict['base']['base']
	else:
		return most_recent_list

def parameterize(command, params, limit, steps, instances):
	# command = CAC command name
	# params = **nested**[parameter name, sub_parameter_name,..]
	error = ''
	# Returns array of CAC instances with parameterized input
	# soft restriction: only edit float type values eg. temp
	base_instance = instances['base']['base'][0]
	base_value = str(base_instance.get_parameter(command, params)
					).replace('d', 'e')
	# Fail if trying to parameterize 'inf'
	if base_value == 'inf':
		error = ("Cannot parameterize 'inf' value")
		return error, instances

	# Adjust delta if vector parameterization [dx, dy, dz]
	if not isinstance(limit, list):
		delta = (float(limit)) / steps
	else:
		delta = [(float(lim)/steps) for lim in limit]

	if command == 'unit_type':
		if not int(delta) == delta:
			error = ("Parameterization causes a non-integer unit_type")
			return error, instances

	if not isinstance(limit, list):
		try:
			base_value = float(base_value)
			limit = float(limit)
		except ValueError:
			error = ("Error while reading parameter for ({})".format(command))
			return error, instances

	# Create the key if first parameterization
	try:
		# First parameterization overall
		if len(instances) == 1:
			instances[command] = {params[-1]: []}

			if not isinstance(limit, list):
				start_val = (base_value)
				# Check values
				if command == 'grain_dir':
					if ((start_val + limit) < 0):
						error = "This parameterization would cause grain_dir overlap to be out of bounds (<0)"
						return error, instances
			else:
				vec_vals = [float(i) for i in split(', |\\[|\\]', base_value)[1:4]]

			# Steps + 1 to include base class
			for i in range(0, steps+1):
				# Duplicate base class values
				temp_class = Cac(base_instance.input)
				temp_class.restart_data_files = base_instance.restart_data_files
				temp_class.output_dir = base_instance.output_dir
				temp_class.potential_files = base_instance.potential_files
				temp_class.add_atom_data_files = base_instance.add_atom_data_files
				# Increment
				if not isinstance(limit, list):
					val= round((start_val + i*delta), 8)

					# Check for odd unit_type:
					if command == 'unit_type':
						if start_val == 1:
							NN = (temp_class.get_parameter('element', ['intpo_depth']))
							if NN%2:
								# start from two
								val = round(2 + (i*delta), 8) if i!=0 else 1
							else:
								val = round((4 + i*delta), 8) if i!=0 else 1
								if val < 4 and i != 0:
									error = "Interpolation depth is 2, unit_type must be 1, or >=4"
								# start from 4
						if val %2 and i!=0:
							error = "This parameterization causes an odd unit_type to be generated"
							return error, instances

					temp_class.description += "-" + command + "_" + "_".join(str(i) for i in params) + "_" + str(val)

				else:
					val = [round((float(list(vec_vals)[j]) + i*delta[j]), 8) for j in range(3)]
					temp_class.description += "-" + command + "_" + "_".join(str(i) for i in params) + "_[" + str(','.join(str(i) for i in val)) + "]"
				#print(temp_class.description)
				temp_class.edit_parameter(command, params, val)
				# Check if modifying basis vectors.
				if command == 'grain_mat':
					g_orient_init = (temp_class.get_parameter(command, params[:-1]))
					norm_g_orient_init = dict()
					for k in g_orient_init:
						norm_g_orient_init[k] = unit(g_orient_init[k])
					# Don't check the base case
					if not vec_vals == val:
						g_orient_final = rotated_bases(vec_vals, val, g_orient_init)
						if (norm_g_orient_init == g_orient_final):
							error = "This parameterization will not change the grain orientation. (Grain: {}, direction: {})".format(*params)
							return error, instances
						else:
							for axis,vec in g_orient_final.items():
								if axis != params[-1]:
									temp_p = [params[0], axis]
									temp_class.edit_parameter(command, temp_p, vec)

				# Add to the list of simulations to run 
				instances[command][params[-1]].append(temp_class)
			return error, instances

		else:
			# First parameterization of new command
			if command not in instances:
				instances[command] = {params[-1]: []}
			if params[-1] not in instances[command]:
				instances[command][params[-1]] = []

			temp_list = []
			
			last = last_edited(instances)

			for inst in last:			
				if not isinstance(limit, list):
					start_val = (base_value)
					# Check values
					if command == 'grain_dir':
						if ((start_val + steps*limit) < 0):
							error = "This parameterization would cause grain_dir overlap to be out of bounds (<0)"
							return error, instances
				else:
					vec_vals = [float(i) for i in split(', |\\[|\\]', base_value)[1:4]]
					# float_lim = [float(j) for j in limit]
					# start_vals = [i - j for i, j in zip(vec_vals, float_lim)]

				for i in range(0, steps+1):
					# Generate from predefined instance
					temp_class = Cac(inst.input)
					temp_class.restart_data_files = inst.restart_data_files
					temp_class.output_dir = inst.output_dir
					temp_class.potential_files = inst.potential_files
					temp_class.description = inst.description
					temp_class.add_atom_data_files = inst.add_atom_data_files
					if not isinstance(limit, list):
						val= round((float(start_val) + i*delta), 8)
						# Check for odd unit_type:
						if command == 'unit_type':
							if start_val == 1:
								NN = (temp_class.get_parameter('element', ['intpo_depth']))
								if NN%2:
									# start from two
									val = round(2 + (i*delta), 8) if i!=0 else 1
								else:
									val = round((4 + i*delta), 8) if i!=0 else 1
									if val < 4 and i != 0:
										error = "Interpolation depth is 2, unit_type must be 1, or >=4"
									# start from 4
							if val %2 and i!=0:
								error = "This parameterization causes an odd unit_type to be generated"
								return error, instances

						temp_class.description += "-" + command + "_" + "_".join(str(i) for i in params) + "_" + str(val) 
					else:
						# Vector increment
						val = [round((float(list(vec_vals)[j]) + i*delta[j]), 8) for j in range(3)]
						temp_class.description += "-" + command + "_" + "_".join(str(i) for i in params) + "_[" + str(','.join(str(k) for k in val)) + "]"
					#print(temp_class.description)
					
					temp_class.edit_parameter(command, params, val)
					# Check if modifying basis vectors.
					if command == 'grain_mat':
						g_orient_init = (temp_class.get_parameter(command, params[:-1]))
						norm_g_orient_init = dict()
						for k in g_orient_init:
							norm_g_orient_init[k] = unit(g_orient_init[k])
						# Don't check the base case
						if not vec_vals == val:
							g_orient_final = rotated_bases(vec_vals, val, g_orient_init)
							if (norm_g_orient_init == g_orient_final):
								error = "This parameterization will not change the grain orientation. (Grain: {}, direction: {})".format(*params)
								return error, instances
							else:
							# Rotate the other vectors accordingly
								for axis,vec in g_orient_final.items():
									if axis != params[-1]:
										temp_p = [params[0], axis]
										temp_class.edit_parameter(command, temp_p, vec)
					temp_list.append(temp_class)

			instances[command][params[-1]] = temp_list
		
		return error, instances

	# except AttributeError:
	# 	print("({}) is not a valid command".format(command))

	except KeyError:
		print("({}) is not a valid parameter of ({})".format(param[0], command))

def write_input(CAC_instance):
	all_commands = [cmd for cmd in vars(CAC_instance.input).keys() if not cmd.startswith("_")]
	command_string_list = []
	for command in all_commands:
		command_string_list.append(CAC_instance.input.parse_command(command))
	
	# Write parsed command strings to file
	try:
		with open(os.path.realpath(CAC_instance.output_dir+ "/" + CAC_instance.description + ".in"), "w+") as fp:
			for command_string in command_string_list:
				#print(command_string)
				fp.write("{0} \n\n".format(command_string))

	except FileNotFoundError:
		shutil.rmtree(os.path.realpath(CAC_instance.output_dir))
		with open(os.path.realpath(CAC_instance.output_dir+ "/" + CAC_instance.description + ".in"), "w+") as fp:
			for command_string in command_string_list:
				#print(command_string)
				fp.write("{0} \n\n".format(command_string))

def build_simulation_directory(pwd, directory_name, cac_list, cluster_home, n_node, n_proc, walltime, batch_type, project_name, queue_name):

	top_level = directory_name.split('/')[-1]

	for simulation in cac_list:
		if len(cac_list) == 1:
			curr_sim_dir = simulation.output_dir
			cluster_sim_dir = cluster_home + top_level + '/'
			fname = os.path.join(curr_sim_dir, simulation.description + ".in")

		else:
			curr_sim_dir = simulation.output_dir + '/' + simulation.description
			cluster_sim_dir = cluster_home + top_level + '/' + simulation.description
			fname = os.path.realpath(curr_sim_dir + ".in")

		os.makedirs(os.path.realpath(curr_sim_dir), exist_ok=True)
		print(curr_sim_dir, cluster_sim_dir)

		# Generate appropriate batch script based on cluster configuration specified during install
		print(batch_type)
		if batch_type == 'torque':
			template_file = 'template.pbs'
			script_file = 'run.pbs'
		elif batch_type == 'slurm':
			template_file = 'template.sl'
			script_file = 'run.sl'
		
		# When running on windows, use universal newlines
		with open(os.path.join(os.path.dirname(pycac.__file__), template_file), 'rU') as in_file, open(os.path.join(os.path.realpath(curr_sim_dir), script_file), 'w+', newline='\n') as out_file:
			for line in in_file:
				line = line.replace("NODES", str(n_node))
				line = line.replace("PROCS", str(n_proc))
				line = line.replace("WALLTIME", str(walltime))
				line = line.replace("QUEUE", str(queue_name))
				line = line.replace("PROJNAME", str(project_name))
				line = line.replace("NTOT", str(n_node*n_proc))
				line = line.replace("CAC_DIR", cluster_sim_dir)
				line = line.replace("CAC_VERS", 'CAC')
				out_file.write(line)

		#shutil.move(os.path.realpath(curr_sim_dir + '/run.pbs'), curr_sim_dir)

		[copy_handler(p, curr_sim_dir) 
			for p in (simulation.potential_files)]

		[copy_handler(r, curr_sim_dir)
			for r in (simulation.restart_data_files)]

		[copy_handler(a, curr_sim_dir)
			for a in (simulation.add_atom_data_files)]

		print(fname)

		shutil.move(fname, os.path.join(curr_sim_dir, 'input.in'))
		print("Built directory structure for {}".format(simulation.description))
	if len(cac_list) != 1:
		proj_path = cac_list[0].output_dir
		files = [os.path.join(proj_path, name) for name in (os.listdir(proj_path))]
		[os.remove(file) for file in files if not os.path.isdir(file)]
		
	# Condense to single tarball
	print("Compressing to " + directory_name + '.tar' )
	with tarfile.open(directory_name + '.tar', 'w') as tar:
		tar.add(directory_name, arcname=top_level)

	n_files = len(cac_list)
	return n_files

def submission_handler(cac_dir, pwd, sim_dir_name, final_sim_list, cluster_home, n_node, n_proc, client, walltime, batch_type, project_name, queue_name):

	n_sims = build_simulation_directory(pwd, sim_dir_name, final_sim_list, cluster_home, n_node, n_proc, walltime, batch_type, project_name, queue_name)
	up_err, extract_dir = up_and_submit_jobs(n_sims, sim_dir_name, cluster_home, cac_dir, client, batch_type)
	up_err = False
	if up_err:
		return(up_err, extract_dir)

	return(0, ["Job(s) submission successful.", extract_dir])

def up_and_submit_jobs(n_sims, sim_dir_name, cluster_home, cac_dir, client, batch_type):
	sftp = client.open_sftp()
	full_sim_path = os.path.realpath(sim_dir_name)
	sim_path, sim_name = os.path.split(full_sim_path)
	local_sim_tar_path = full_sim_path + ".tar"
	sim_tar_name = sim_name + ".tar"
	if os.path.isfile(local_sim_tar_path):
		print("Attempting upload of job data to cluster...")
		# tar file name, not directory
		err, stat = upload(sftp, local_sim_tar_path, cluster_home+sim_tar_name)
		if err:
			sftp.close()
			return(1, stat)
		else:
			print("\t{}".format(stat))
	else:
		stat = ("Couldn't find the specified tar file on{}".format(local_sim_tar_path))
		print("\t{}".format(stat))

	extract_dir = cluster_home + sim_name
	print("Extracting to: " + extract_dir)

	if not cluster_home:
		untar = 'tar -xf ' + sim_tar_name 
	else:
		untar = 'tar -xf ' + cluster_home + sim_tar_name + ' -C ' + cluster_home
	client.exec_command(untar)

	# Slight delay in waiting on tar to extract all files
	n_extracted = 0
	n = 1
	if n_sims != 1:
		while n_extracted != n_sims: 
			try:
				sub_dirs = (sftp.listdir(extract_dir))
				n_extracted = len(sub_dirs)
			except FileNotFoundError:
				print("\tTar working...")
				time.sleep(n)
				n += 1
	else:
		while n_extracted != len(os.listdir(full_sim_path)): 
			try:
				sub_dirs = [extract_dir]
				n_extracted = len(sftp.listdir(extract_dir))
			except FileNotFoundError:
				print("\tTar working...")
				time.sleep(n)
				n += 1
	prune_tar = 'rm ' + cluster_home + sim_tar_name
	print(prune_tar)
	client.exec_command(prune_tar)

	extract_dir = cluster_home + sim_name
	# print("extract_dir: " + extract_dir)
	cac_dir = '/'+cac_dir.strip('/')+'/'
	print(sub_dirs)
	for single_sim in sub_dirs:
		# Copy installed CAC to each run directory
		if len(sub_dirs) != 1:
			sim_path = extract_dir + '/' + single_sim
		else:
			sim_path = extract_dir

		cac_path = cac_dir + 'CAC'
		try:
			sftp.stat(cac_path)
		except IOError as e: 
			if e.errno == errno.ENOENT:
				print(cac_path)
				return(1, "CAC simulator was not found on path specified in config file.")
		print("...\n")
		print("Executing job submission for {}".format(single_sim))
		copy_cac = 'cp ' + cac_dir + 'CAC' + ' ' + sim_path
		print("\t{}".format(copy_cac))
		client.exec_command(copy_cac)
		
		print(batch_type)
		if batch_type == 'torque':
			script_path = sim_path + '/run.pbs'
			print('\tqsub ' + script_path)
			exec_batch = 'qsub ' + script_path
		elif batch_type == 'slurm':
			script_path = sim_path + '/run.sl'
			print('\tsbatch ' + script_path)
			exec_batch = 'sbatch ' + script_path

		# Wait for cluster to register submission or rate limit errors occur
		stdin, stdout, stderr = client.exec_command(exec_batch, get_pty=True)
		stdout.readlines()

	sftp.close()
	os.remove(local_sim_tar_path)
	return(0, extract_dir)

def collect_and_submit(base_instance, host, user, password, paramList, n, ppn, cluster_dir, walltime, project_name, queue_name):

	build_errors = []

	if not walltime:
		build_errors.append("Walltime must be a nonzero value (HH:MM:SS)")
	if not n:
		build_errors.append("Nodes must be a nonzero value")
	if not ppn:
		build_errors.append("Processors per Node must be a nonzero value")

	pwd = os.getcwd()

	#Verify install has been executed by user
	try:
		with open(os.path.realpath(pwd+'/config.json'), 'r') as infile:
			config = json.load(infile)
	except FileNotFoundError:
		base_instance.input.errors.append("Config file is missing; please run the setup application prior to creating a CAC job")

	# Build test directory structure locally
	d = datetime.datetime.now()
	timestamp = d.strftime("%Y/%m/%d-%H:%M")
	sim_dir_name = base_instance.output_dir

	# Always build and populate the base instance from initial output

	simulations = {'base': {'base': [base_instance]}}

	simulations['base']['base'][0].description = "singlerun"

	for param_set in paramList:
		error, simulations = parameterize(*param_set, simulations)
		if error:
			build_errors.append(error)

	print("Creating directory ({})".format(base_instance.output_dir))
	os.makedirs(base_instance.output_dir, exist_ok=True)


	# MUST use the last edited command
	final_sim_list = last_edited(simulations)

	# Write potential paths, write input file
	for cac in final_sim_list:
		write_input(cac)

	# Transfer simulation archive using ssh_util and extract
	if not cluster_dir:
		cluster_home = ''
	else:
		cluster_home = cluster_dir.strip('/')+'/'

	conn_err, connection = login(host, user, password)

	if len(build_errors)>0: 
		if conn_err:
			build_errors.append(connection)
		return(1, build_errors)

	if not conn_err:
		err, upload_stat = submission_handler(config['install']['cac_path'], pwd+'/', sim_dir_name, final_sim_list, cluster_home, n, ppn, connection, walltime, config['install']['job_type'], project_name, queue_name)
		connection.close()
		# only record on sucessful submission
		for t, paths in config['run_log'].items():
			if paths == [sim_dir_name, upload_stat[1]]:
				config['run_log'].pop(t)
				print("Duplicate local and cluster locations. Updated to most recent run")
		# Record and write to file
		config['run_log'][timestamp] = [sim_dir_name, upload_stat[1]]
		with open('config.json', 'w') as updatefile:
			json.dump(config, updatefile)

		if err:
			return(1, [upload_stat])
		else:
			return(0, ["Successfully submitted jobs"])
	else:
		build_errors.append(connection)
		return(1, build_errors)

## LOCAL input creation

def build_local_simulation_directory(cac_list):
	# Same as build_simulation_directory but no PBS files are created
	for simulation in cac_list:
		if len(cac_list) == 1:
			curr_sim_dir = simulation.output_dir
			in_file = os.path.join(curr_sim_dir, simulation.description + ".in")
		else:
			curr_sim_dir = simulation.output_dir + '/' + simulation.description
			in_file = os.path.realpath(curr_sim_dir + ".in")
			if os.path.exists(os.path.realpath(curr_sim_dir)):
				shutil.rmtree(os.path.realpath(curr_sim_dir))
			os.mkdir(os.path.realpath(curr_sim_dir))

		print(curr_sim_dir)

		[copy_handler(p, curr_sim_dir) 
			for p in (simulation.potential_files)]

		[copy_handler(r, curr_sim_dir)
			for r in (simulation.restart_data_files)]

		[copy_handler(a, curr_sim_dir)
			for a in (simulation.add_atom_data_files)]
		
		print(in_file)
		shutil.move(in_file, os.path.join(curr_sim_dir, 'input.in'))

		print("Built directory structure for {}".format(simulation.description))

def generate_local_input(base_instance, paramList):
	# ONLY create input file locally, same as generate_local_input
	pwd = os.getcwd()

	# Build test directory structure locally
	d = datetime.datetime.now()
	timestamp = d.strftime("%Y/%m/%d-%H:%M")
	sim_dir_name = base_instance.output_dir

	# Always build and populate the base instance from initial output
	simulations = {'base': {'base': [base_instance]}}

	simulations['base']['base'][0].description = "RUN_single"

	build_errors = []

	# parameterization
	for param_set in paramList:
		error, simulations = parameterize(*param_set, simulations)
		build_errors.append(error)

	os.makedirs(base_instance.output_dir, exist_ok=True)
	print("Creating directory ({})".format(base_instance.output_dir))

	# MUST use the last edited command!!
	final_sim_list = last_edited(simulations)

	# Write potential paths, write input file
	for cac in final_sim_list:
		write_input(cac)


	build_local_simulation_directory(final_sim_list)

	if paramList:
		proj_path = base_instance.output_dir
		files = [os.path.join(proj_path, name) for name in (os.listdir(proj_path))]
		[os.remove(file) for file in files if not os.path.isdir(file)]

	if len(build_errors) > 0 and build_errors[0]:
		return(1, build_errors)
	else:
		return(0, ["Succesfully built local project folder(s)"])


if __name__ == "__main__":
	main()
