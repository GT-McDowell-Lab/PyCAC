#title:downloads.py
#description: utilities for downloading project data from cluster
#author:chu.k@gatech.edu
#updated:2018/06/26
#version:0.1
#usage:N/A
#notes:McDowell Lab PyCAC.
#python_version:3.6.4
# =============================================================================

from .ssh_util import login, download, tar_remote
from .vtk2dump import converter

import os, sys, datetime
import json
import tarfile
import getpass
import random
import glob

def load_config():
	# config file must be on current path
	local_path = os.getcwd()
	config_path = os.path.realpath(os.path.join(local_path, 'config.json'))
	try:
		with open(config_path, 'r') as cfg_file:
			config = json.load(cfg_file)
	except FileNotFoundError:
		return(1, "Config file not found on current path")

	return(0, config)

def get_recent_projects(n):
	# Returns n entries of config.json run_log
	error, dat = load_config()
	if error:
		return(error, dat)
	limit = 0

	full_log = dat['run_log']
	truncated_log = dict()

	# Sort on datetime custom formatted string
	most_recent = list(sorted(full_log.keys(), key = lambda x: datetime.datetime.strptime(x, '%Y/%m/%d-%H:%M'), reverse=True))

	for timestamp in most_recent:
		if limit >= n:
			break
		else:
			truncated_log[timestamp] = full_log[timestamp]
			limit += 1

	if not truncated_log:
		return(1, "Empty run log. No jobs submitted through PyCAC")

	return(0, truncated_log)


def download_project(host, user, passwd, local_dir, cluster_dir):

	conn_err, connection = login(host, user, passwd)
	if not conn_err:
		# Tar up directory on cluster if exists (which it should since you created it and added it to config.json)
		tar_err, cluster_tar_path = tar_remote(connection, cluster_dir)
		if tar_err:
			return(tar_err, cluster_tar_path)
		#cluster_tar_path = "/nv/hp28/kchu41/data/test1_data.tar"
		file_name = os.path.basename(cluster_tar_path)
		down_err, path = download(connection, cluster_tar_path, os.path.realpath(local_dir+'/'+file_name))
		#down_err, path = (0, "/mnt/c/Users/kchu41/Documents/CAC/pycac_0.1_dist/test1/test1_data.tar")
		if not down_err:
			print("Extracting project data to " + local_dir)
			project = tarfile.open(path)
			project.extractall(local_dir)
			project.close()
			print("Finished extracting")
			return (down_err, local_dir)
		else:
			return(1, path)
	
	return (conn_err, connection)

def extract_timestep(project_directory):
	# Enters project directory and searches for cac_atom_*.vtk, cac_atom_*.vtk files to extract timesteps
	vtk_list = []
	[vtk_list.append(vtk_f) for vtk_f in glob.glob1(project_directory, "cac_*vtk")]
	step_list = []
	[step_list.append(int(p.split('.vtk')[0].split('_')[-1])) for p in vtk_list if int(p.split('.vtk')[0].split('_')[-1]) not in step_list]

	if not step_list:
		return(1, "VTK files were not found. Project does not exist, or the simulations were not run by the cluster")
	else:
		return(0, step_list)

def convert_timestep(local_project_directory, timestep, params):
	return converter(local_project_directory, timestep, params, 8, 1)


def main():

	error, log = get_recent_projects(4)
	
	time, dirs = random.choice(list(log.items()))
	local = dirs[0]
	cluster = dirs[1]

	if error:
		print(log)

	local = os.path.realpath(os.getcwd() + '/test')
	#down_stat, project_path = (download_project("granulous.pace.gatech.edu", "kchu41", passwd, local, 'data/test'))

	print(extract_timestep(local))

	selected = [0]




if __name__ == "__main__":
	main()