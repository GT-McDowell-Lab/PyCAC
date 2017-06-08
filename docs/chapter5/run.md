## run

### Syntax

	run total_step time_step

* `total_step` = non-negative integer

* `time_step` = positive real number

### Examples

	run 10000 0.002

### Description

This command sets the total step and time step of a CAC simulation.

`total_step` is the total time step of dynamic CAC, the total loading increment of quasistatic CAC, or the total time step of the dynamic part in hybrid CAC.

`time_step`, in unit of ps, is the time step in dynamic CAC simulations or the dynamic part in hybrid CAC simulations.

### Related commands

`time_step` becomes irrelevant when [simulation_style](simulator.md) = _statics_.

When [`boolean_restart`](restart.md) = _t_, the `total_step` is added to the time stamp read from the `cac_in.restart` file, instead of overriding it.

### Related files

`dynamics_init.f90`, `dynamics.f90`, and `hybrid.f90`.

### Default

	run 0 0.002