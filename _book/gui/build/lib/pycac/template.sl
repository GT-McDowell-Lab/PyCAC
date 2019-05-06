#!/bin/bash -l

# SBATCH script

#SBATCH -J PROJNAME
#SBATCH -N NODES
#SBATCH --ntasks-per-node=PROCS
#SBATCH -t WALLTIME
#SBATCH -p QUEUE


cd $HOME/CAC_DIR

mpirun -np NTOT ./CAC_VERS < input.in
