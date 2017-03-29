## dump

### Syntax

	dump output_freq reduce_freq restart_freq log_freq

* output\_freq, reduce\_freq, restart\_freq, log\_freq = integer

### Examples

	dump 500 300 1000 10

### Description

Set the frequency by which the output is performed. For example, when a certain frequency is 100, the corresponding output is conducted when the time step is divisible by 100.

output\_freq is related to the `dump.#` files (readable by [OVITO](http://www.ovito.org/)) and the `*.vtk` files (readable by [ParaView](http://www.paraview.org/)), see the [Post-processing](post-processing.md) chapter for more information about the visualization in PyCAC.

reduce\_freq is related to certain `MPI_reduce` quantities in the `cac.log` file.

restart\_freq is related to the `cac_out_#.restart` files.

Like reduce\_freq, log\_freq is also related to the `cac.log` file, while the latter only outputs one line to monitor where the simulation is at.

### Related commands

None.

### Related files

`dump_init.f90` and `dump.f90`

### Default

	dump 1000 1000 5000 50