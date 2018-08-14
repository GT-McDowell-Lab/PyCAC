#!/usr/bin/env python
#title:install.py
#description:install cac from source onto user cluster
#					
#author:chu.k@gatech.edu
#updated:2018/06/18
#version:0.2
#usage:N/A
#notes:McDowell Lab PyCAC. Version req for dictionary order preservation
#python_version:3.6.4
#=============================================================================
from .ssh_util import upload, login
import os, sys, json
from time import sleep
import pycac

def prompt_overwrite():
	while (True):
		response = input("Overwrite? (y/n): ")
		if response in ['y', 'yes']:
			return True
		elif response in ['n', 'no']:
			return False

def exec_cluster_commands(client, directory, cac_source):
	cac_source_dir, cac_ext = os.path.splitext(cac_source)
	if cac_ext != '.tar':
		return(1, "The CAC source should be bundled as TAR file.")
	ftp = client.open_sftp()
	stdin, stdout, stderr = client.exec_command("echo $HOME", get_pty=True)
	for line in iter(stdout.readline, ""):
		home_dir = line.splitlines()
	cluster_full_path = home_dir[0] + '/' + directory
	install_file_path = cluster_full_path + "/cac.tar"
	try:
		if ftp.listdir(cluster_full_path):
			return(1, "Warning, a version of CAC exists in this directory... install aborted")

	except FileNotFoundError:
		ftp.mkdir(cluster_full_path)

	if os.path.isfile(os.path.realpath(cac_source)):
		err, stat = upload(ftp, os.path.realpath(cac_source), install_file_path)
	else:
		print(os.path.dirname(pycac.__file__))
		return(1, "Unsuccessful, CAC package is missing from your PyCAC install.")

	untar = 'tar -xf ' + install_file_path + ' -C ' + cluster_full_path
	cd_install = 'cd ' + cluster_full_path + '; ./install.sh'
	client.exec_command(untar)

	# Wait for tar to finish
	while (len(ftp.listdir(cluster_full_path)) != 4):
		print("Unpacking...")
		sleep(1)

	print("Attempting install...")
	stdin, stdout, stderr = client.exec_command(cd_install, get_pty=True)
	
	for line in iter(stdout.readline, ""):
		print(line, end="")

	# Check for install success
	try:
		if ftp.listdir(cluster_full_path + '/build/'):
			return(0, (cluster_full_path + '/build/'))
		else:
			return(1, "Errors encountered while building. Check that mpif90 exists on the cluster.")
	except FileNotFoundError:
			return(1, "Errors encountered while building. No build directory detected")

def run_install(host, user, password, install_path, job_type, cac_source):
	'''
	install_path is the path relative to $HOME on the cluster. 
	'''
	directory = '/'.join(install_path.split('/'))

	conn_err, connection = login(host, user, password)

	if not conn_err: 
		error_status = (exec_cluster_commands(connection, install_path, cac_source))
		connection.close()
	else:
		return(1, connection)

	if not error_status[0]:
		config = {'install' : 
					{'server': host, 
					 'user': user, 
					 'cac_path': error_status[1],
					 'job_type': job_type },
			  'run_log': {}
			 }
		with open('config.json', 'w') as outfile:
			json.dump(config, outfile)
			print('Config file generated ({})'.format((os.getcwd()+'/config.json')))
		path_string = user+"@"+host+':'+ error_status[1]
			
		return(0, "Successfully built CAC on " + path_string)


	return error_status

if __name__ == "__main__":
	main()