## dump

### Syntax

	dump output_freq reduce_freq restart_freq log_freq

* `output_freq`, `reduce_freq`, `restart_freq`, `log_freq` = positive integer

### Examples

	dump 500 300 1000 10

### Description

This command sets the frequency with which the output is performed. For example, when a certain frequency is 100, the corresponding output is conducted when the total step is divisible by 100.

`output_freq` sets the frequency with which the `dump.#` files (readable by [OVITO](http://www.ovito.org/)) and the `*.vtk` files (readable by [ParaView](http://www.paraview.org/)) are written to the disk system. The user may then [post-process](../chapter6/README.md) these files for visualization purpose and for further analysis.

`reduce_freq` sets the frequency with which certain quantities are written to `group_cal_#` (when [`cal_number`](group_num.md) > 0) and`cac.log` by [root](rank.md), which [MPI_Reduce](http://mpitutorial.com/tutorials/mpi-reduce-and-allreduce)s relevant information from other processors.

`restart_freq` sets the frequency with which the `cac_out_#.restart` files are written to the disk system. These files can be read to [restart](restart.md) simulations.

`log_freq` sets the frequency with which one line is written to the `cac.log` file and the screen to monitor the simulation progress.

### Related commands

None.

### Related files

`dump_init.f90` and `dump.f90`

### Default

	dump 1000 1000 5000 50
