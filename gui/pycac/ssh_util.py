#!/usr/bin/env python
#title:ssh_util.py
#description:compute cluster ssh methods for job submission
#					
#author:chu.k@gatech.edu
#updated:2018/07/03
#version:0.2
#usage:N/A
#notes:McDowell Lab PyCAC.
#python_version:3.6.4
#==============================================================================

import paramiko
import errno
import os

def connect(host, user, passwd):
	ssh_client = paramiko.SSHClient()
	ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
	try:
		ssh_client.connect(hostname=host,username=user,password=passwd)
	except BlockingIOError:
		return(1, "Unable to communicate with server.")
	return(0, ssh_client)

def login(host, user, passwd):
	ssh_client = paramiko.SSHClient()
	ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
	try:
		ssh_client.connect(hostname=host,username=user,password=passwd)
		return(0, ssh_client)
	except (BlockingIOError, OSError):
		return(1, "Unable to communicate with server. Verify server address and network configuration")
	except paramiko.ssh_exception.AuthenticationException:
		return(2, "Wrong username or password")

def mkdir_p(sftp, remote, is_dir=False):
	# Makes directory tree if doesn't exist on cluster
	dir_tree = []
	if is_dir:
		tree = remote
	else:
		tree, leaf = os.path.split(remote)
	# Split down to the base directory, tracking the tree as it's shortened
	while len(tree) > 1:
		dir_tree.append(tree)
		tree, leaf = os.path.split(tree)

	# Catch the case for relative pathing to $HOME on the cluster
	if len(tree) == 1 and not tree.startswith('/'):
		dir_tree.append(tree)

	while len(dir_tree):
		leaf = dir_tree.pop()
		try:
			sftp.stat(leaf)
		except:
			print("Mkdir: {}".format(leaf))
			sftp.mkdir(leaf)

def upload(sftp, files, directory):
	#print("Uploading: {}".format(files))
	# Run directory exists. 

	if exists(sftp, directory):
		return(1, "Project of the same name exists, click 'back' and modify the name")

	if isinstance(files, list):
		for file in files:
			sftp.put(file, directory)
	else:
		mkdir_p(sftp, directory)
		try:
			sftp.put(files, directory)
		except IOError:
			return(1, "Failed to put")

	return(0, "Upload success")

def download(ssh_client, cluster_tar, local_file_name):
	# cluster_tar needs to be a full path
	sftp = ssh_client.open_sftp()
	if not exists(sftp, cluster_tar):
		return(1, "Specified file {} does not exist".format(cluster_tar))
	local_folder = os.path.dirname(local_file_name)
	info = sftp.stat(cluster_tar).st_size
	if not os.path.isdir(local_folder):
		print("Creating local download directory " + local_folder)
		os.mkdir(local_folder)
		#return(2, "Specified local download location has not been created")
	# Passed checks
	print("Downloading to " + local_file_name)
	print("This may take a few minutes. Data file size is: " + str(info) + "B")
	sftp.get(cluster_tar, local_file_name)
	sftp.close()

	return(0, local_file_name)

def tar_remote(ssh_client, cluster_folder):
	stdin, stdout, stderr = ssh_client.exec_command("echo $HOME", get_pty=True)
	for line in iter(stdout.readline, ""):
		home_dir = line.splitlines()
	cluster_full_path = home_dir[0] + '/' + cluster_folder
	sub_dir_name = os.path.basename(cluster_full_path)
	sftp = ssh_client.open_sftp()
	if not exists(sftp, cluster_full_path):
		return(1, "Specified project directory {} does not exist".format(cluster_full_path))

	file_name = cluster_full_path + '_data.tar'

	tar_string = 'tar -cvf ' + file_name + ' -C ' + cluster_full_path.split(sub_dir_name)[0] + ' ' + sub_dir_name
	print("Compressing to " + file_name)
	stdin, stdout, stderr = ssh_client.exec_command(tar_string)
	for line in iter(stdout.readline, ""):
		print(line, end="")

	sftp.close()
	return (0, file_name)

def exists(sftp, path):
	try:
		sftp.stat(path)
	except IOError as e: 
		if e.errno == errno.ENOENT:
			return False
		raise
	else:
		return True
	
