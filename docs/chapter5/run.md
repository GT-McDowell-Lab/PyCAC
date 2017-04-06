## run

### Syntax

	run total_step time_step

* total\_step = non-negative integer

* time\_step = real number

### Examples

	run 10000 0.002

### Description

Set the style of running CAC.

`total_step` is the total time step of dynamic CAC, or the total increment of quasistatic CAC, or the total time step of dynamic simulations in hybrid CAC.

`time_step`, in unit of ps, is the time step for dynamic or hybrid CAC.

Note that if the model is read from a `cac_in.restart` file, the `total_step` is added to the time stamp of the restart file, instead of overriding it.

### Related commands

The meaning of the `total_step` depends on the [simulator](simulator.md).

### Related files

`dynamics_init.f90`, `dynamics.f90`, `hybrid.f90`, among many

### Default

`time_step` = 0.002