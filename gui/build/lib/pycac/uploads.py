# title:uploads.py
# description:utilities for uploading existing project data to cluster
# author:chu.k@gatech.edu
# updated:2018/07/04
# version:0.1
# usage:N/A
# notes:McDowell Lab PyCAC. Version req for dictionary order preservation
# python_version:3.6.4
# =============================================================================
from os.path import realpath, join, split, isfile, dirname, isdir
from datetime import datetime
from os import listdir, rename, remove
from glob import glob, glob1
from re import sub
from shutil import copy
import tarfile, json, sys

from .CacClass import Cac
from .downloads import load_config
from .interface import up_and_submit_jobs
from .ssh_util import login
import pycac

import pdb
from PyQt5.QtCore import *

def project_folder_check(projectpath):
    '''
    Check a project folder structured as follows:
    |-projectpath/
    |-----|Run1/
    |-----|----|input.in
    |-----|----|potential files (*.tab or *.lj)
    |-----|----|restart files(optional)
    |-----|Run2/
    ....
    '''
    project_path = realpath(projectpath)
    proj_dict = {join(project_path, proj) : listdir(join(project_path, proj)) for proj in listdir(project_path) if isdir(join(project_path, proj))}
    print(proj_dict)

    # Assume CAC simulator is installed on the cluster, will read config for the location. 
    proj_instances = dict()
    print("Checking input files:")
    for run, files in proj_dict.items():
        print("\t{}".format(split(run)[1]))
        error, val = single_run_check(run, files)
        if error:
            return(error, val)
        else:
            val.description = split(run)[1]
            proj_instances[val.description] = val
    # Check all project runs for errors
    error_tracker = []

    # Consolidate all parsing errors. 
    for run, obj in proj_instances.items():
        has_errors, err_list = obj.get_errors()
        if has_errors:
            error_tracker.append((run, obj))

    # Return cac object if NONE of the runs have errors
    if not error_tracker:
        return(0, list(proj_instances.values()))
    else:
        return(1, error_tracker)

def single_run_check(runpath, files):
    proj, basename = split(runpath)
    input_path = [join(runpath, input) for input in glob1(runpath, "*.in")]
    input_error, vals = input_file_check(input_path)
    if input_error:
        return(2, vals+runpath)

    # Generate the base instance as in InputWidget

    # Input file MUST have all these commands
    unset_commands = ['simulator', 'minimize','grain_num', 'zigzag',
                   'grain_mat', 'subdomain', 'unit_type', 'unit_num', 
                   'box_dir', 'boundary', 'modify_num', 'potential',
                   'lattice', 'mass', 'run', 'dump', 'deform', 'group_num', 'refine']
    base_cac = Cac()
    for cmd, params in vals:
        base_cac.edit_command(cmd, params)
        try:
            unset_commands.remove(cmd)
        except ValueError:
            pass
    if unset_commands:
        return(3, "Input file is incomplete, the following commands are missing: {}".format(', '.join(unset_commands)))

    # Check current project directory for required files
    base_cac.set_output(proj)
    # Alternate set restart for an exsiting directory (no renames req.)
    restart_err, val = base_cac.set_restart_exists(runpath)
    if restart_err:
        return(restart_err, val)
    base_cac.set_potential(runpath)
    
    base_cac.check_dependencies()
    print(base_cac.get_errors())


    if not glob1(runpath, "*.pbs") and not glob1(runpath, "*.sl"):
        print("\t>>Missing batch script for job: {}".format(basename))
    
    #pbs_error, vals = pbs_file_check(pbs_path)

    return(0, base_cac)

def input_file_check(inputpath):
    if len(inputpath) > 1:
        return(1, "Multiple input files with file ending *.in found in the run folder: ")
    elif len(inputpath) == 0:
        return(1, "There were no input files found in the run folder: ")
    else:
        inputpath = inputpath[0]
    path, basename = split(inputpath)
    param_list = []
    try:
        with open(inputpath, 'r') as fp_in:
            subdomains =  []
            for line in fp_in:
                if line.strip() and line.strip()[0] != '#':
                    line_a = line.split()
                    cmd = line_a[0]
                    params = line_a[1:]
                    for tup in convert_vals(cmd, params, subdomains):
                        if tup[0] == 'suberr':
                            return(1, "Error in subdomain command, discrepancy between defined subdomains and unit_type, unit_num for input script in: ")
                        param_list.append(tup)
                        if tup[0] == 'subdomain':
                            subdomains.append(tup[1][1])
        return(0, param_list)
    # Shouldn't be triggered but doesn't hurt to check
    except FileNotFoundError:
        print(path)
        return(1, "There were no input files found in the project folder")

def convert_vals(cmd, params, subdomains):
    # Convert to floats and ints where necessary
    for i, val in enumerate(params):
        if val != 'inf':
            try:
                params[i] = int(val)
            except ValueError:
                try:
                    params[i] = float(val)
                except ValueError:
                    # Fall through to string
                    pass
    # Multigrain commands require "splitting" due to backend structure
    cmd_split = []
    # Look at InputClass.py for where std_len values come from
    if cmd == 'grain_mat':
        std_len = 13
    elif cmd == 'grain_move':
        std_len = 4
    elif cmd == 'subdomain':
        std_len = 2
    elif cmd == 'unit_type' or cmd == 'unit_num':
        if cmd == 'unit_type':
            sub_p = 2
        elif cmd == 'unit_num':
            tmp_params = []
            sub_p = 4
            [tmp_params.append(p) for p in params if not (isinstance(p, str))]
            params = tmp_params
        # len(subdomains) == number of grains. each index is number of 
        # subdomains in its corresponding index+1 grain. 
        new_params = []
        prev = 0

        # Check consistency in number of subdomains defined in unit_num/type
        expected = len(subdomains)
        for n_sub in subdomains:
            expected += n_sub*sub_p
        if len(params) != expected:
            return([('suberr', n_sub)])

        for i, n in enumerate(subdomains):
            start = i+sub_p*prev
            prev = subdomains[i]
            while n > 0:
                # Some ugly list splicing to get grain num, and subdomain 1,2,...n for all grains. 
                new_params.append((cmd, [params[start], *params[sub_p*n-(sub_p-1)+start:sub_p*n+1+start]]))
                n -= 1
        return(new_params)
    else:
        # Normal command. Just return after conversion
        if cmd == 'box_dir':
            return([(cmd, [p for p in params if not (isinstance(p, str))])])
        return([(cmd, params)])

    # Split and create new command tuples.
    num_split = int(len(params)/std_len)
    for i in range(num_split):
        cmd_split.append((cmd,params[i*std_len:(i+1)*std_len]))
    return(cmd_split)

def generate_batch(runpath, cluster_dir, n_node, ppn, walltime, single, job_type, project_name, queue_name):
    # template.pbs/.sl installed with pycac
    if job_type == 'torque':
        file_ext = ".pbs"
    elif job_type == 'slurm':
        file_ext = ".sl"

    template_file = join(dirname(pycac.__file__), 'template'+ file_ext)
    projpath, run = split(runpath)
    base, projname = split(projpath)

    if single:
        cluster_sim_dir = cluster_dir +  run
    else:    
        cluster_sim_dir = cluster_dir + projname + '/' + run
    
    run_file = (join(runpath,'run'+file_ext))
    print(run_file)

    if isfile(template_file):
        with open(template_file, 'rU') as in_file, open(run_file, 'w+', newline='\n') as out_file:
            for line in in_file:
                line = line.replace("NODES", str(n_node))
                line = line.replace("PROCS", str(ppn))
                line = line.replace("WALLTIME", str(walltime))
                line = line.replace("QUEUE", str(queue_name))
                line = line.replace("PROJNAME", str(project_name))
                line = line.replace("NTOT", str(n_node*ppn))
                line = line.replace("CAC_DIR", cluster_sim_dir)
                line = line.replace("CAC_VERS", 'CAC')
                out_file.write(line)
        return(0, run_file)
    else:
        print(dirname(pycac.__file__))
        return(1, "Unsuccessful, batch script template{} file is missing from install.".format(file_ext))

def batch_file_check(batchpath, remote, job_type):
    if job_type == 'torque':
        file_ext = ".pbs"
    elif job_type == 'slurm':
        file_ext = ".sl"

    run_dir, file = split(batchpath)
    proj_dir, run = split(run_dir)
    base, proj = split(proj_dir)
    print("\t{}".format(run))
    # Do NOT convert to realpath, cluster typically not Windows path strings
    abs_path = '$HOME/'+ remote + proj + '/'+ run
    cluster_cd = 'cd ' + abs_path+'\n'
    # Open PBS script and verify cd into correct dir
    temp_file = join(base, "run{}.tmp".format(file_ext))
    edited = False
    with open(batchpath, 'rU') as batch_fp, open(temp_file, 'w+', newline='\n') as tmp_fp:
        for line in batch_fp:
            if line.startswith('cd '):
                if (cluster_cd.strip() != line.strip()):
                    print("\t--editing {}".format(join(run, file)))
                    edited = True
                    line = cluster_cd
            tmp_fp.write(line)
    try:
        rename(temp_file, batchpath)
    except FileExistsError:
        remove(pbspath)
        rename(temp_file, batchpath)
    return((run_dir, edited))


def upload_project(projectpath, remote_path, client, n_node, ppn, walltime, project_name, queue_name):
    # Check that remote_path matches the PBS "cd dir" line
    if not remote_path:
        remote_path = ''
    else:
        remote_path = remote_path.strip('/') +'/'

    # load config values
    cfg_error, config = load_config()
    if cfg_error:
        return(1, config)
    cac_dir = config['install']['cac_path']
    cac_dir = '/'+cac_dir.strip('/')+'/'
    job_type = config['install']['job_type']
    if job_type == 'torque':
        file_ext = ".pbs"
    elif job_type == 'slurm':
        file_ext = ".sl"


    print("...\nStarting upload steps...")
    projectpath = realpath(projectpath)
    base, proj_name = split(projectpath)
    runs = listdir(projectpath)
    
    # Clean batch file from search list
    try:
        runs.remove('run.pbs')
    except ValueError:
        try:
            runs.remove('run.sl')
        except ValueError:
            pass

    single = False
    for run in runs:
        if not isdir(join(projectpath,run)):
            single=True
            runs=[projectpath]
            break

    print("Checking batch scripts:")
    edits = []

    if single:
        runpath = projectpath
        batch_file = glob1(runpath, "*"+file_ext)
        if not batch_file:
            err, val = generate_batch(runpath, remote_path, n_node, ppn, walltime, single, job_type, project_name, queue_name)
            if err:
                return(err, val)
            else:
                print("\t Created new batch script: {}".format(val))
    else:        
        for run in runs:
            batch_file = []
            runpath = join(projectpath, run)
            batch_file = [join(runpath, f) for f in glob1(runpath,"*"+file_ext)]
            # No PBS script, make one
            if not batch_file:
                err, val = generate_batch(join(projectpath, run), remote_path, n_node, ppn, walltime, single, job_type, project_name, queue_name)
                if err:
                    return(err, val)
                else:
                    print("\t Created new batch script: {}".format(val))
            # Check validity
            else:
                edits.append(batch_file_check(batch_file[0], remote_path, job_type))

    # Prepare tarball
    print("...\nCreating project package...")
    local_sim_tar = projectpath+'.tar'
    with tarfile.open(local_sim_tar, 'w') as proj_tar:
        proj_tar.add(projectpath, arcname=proj_name)
    print("\t{}".format(local_sim_tar))

    # Upload
    print("...\nStarting cluster submission...")
    
    print("({}) jobs in project".format(len(runs)))
    up_err, extract_dir = up_and_submit_jobs(len(runs), projectpath, remote_path, cac_dir, client, job_type)

    if up_err:
        return(up_err, extract_dir)

    print("...\n Updating log file and cleaning up...")

    # Update config log
    d = datetime.now()
    timestamp = d.strftime("%Y/%m/%d-%H:%M")
    config['run_log'][timestamp] = [projectpath, extract_dir]
    with open('config.json', 'w') as updatefile:
        json.dump(config, updatefile)

    return(0, ["Job(s) submission successful.", extract_dir])

def overwrite_input(input_file, cac_instance):
    print("OVERWRITING : " + input_file)
    all_commands = [cmd for cmd in vars(cac_instance.input).keys() if not cmd.startswith("_")]
    command_string_list = []
    for command in all_commands:
        command_string_list.append(cac_instance.input.parse_command(command))

    with open(input_file, 'w+') as in_fp:
        for command_string in command_string_list:
            in_fp.write("{} \n\n".format(command_string))


def main():
    folder ='/home/chuk/gt-cloud/Research/PyCAC/Projects/restartmulti'
    #err, val = (single_run_check(folder, listdir(folder)))
    err, stat = project_folder_check(folder)
    print(err, stat)

    if not err:
        # Pass base case to InputWidget GUI
        err, stat = upload_project(folder, 'data/1/2/3', 'conn', 2, 3,'01:23:45', 'newname')
        if err:
            print(stat)

    # # Err 1 is input field problems
    # elif err == 1:
    #     print("Errors detected for the following runs:")
    #     for run, errs in val:
    #         print("\t RUN:{}\n\t ERRORS:".format(run))
    #         [print("\t\t{}".format(err)) for err in errs]
    # # Err 2 is project directory issues
    # elif err ==2:
    #     print(val)

if __name__ == "__main__":
    main()