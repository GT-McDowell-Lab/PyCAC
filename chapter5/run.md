## run

### Syntax

	run total_step time_step

* `total_step` = non-negative integer

* `time_step` = positive real number

### Examples

	run 10000 0.002

### Description

This command sets the total step and time step of a CAC simulation.

`total_step` is the total simulation step of dynamic/hybrid CAC simulations or the total loading increment of quasistatic CAC simulations.

`time_step`, in ps, is the time step in [dynamic CAC](dynamics.md) simulations, dynamic part in hybrid CAC simulations, and some quasistatic simulations when [`mini_style`](minimize.md) = _fire_ or _qm_. It is also used in the [fix](fix.md) command when `assign_style` = _disp_.

### Related commands

`time_step` becomes irrelevant when [`simulation_style`](simulator.md) = _statics_ with [`mini_style`](minimize.md) = _cg_ or _sd_.

When [`boolean_restart`](restart.md) = _t_, the `total_step` is added to the time stamp read from the `cac_in.restart` file, instead of overriding it.

### Related files

`dynamics_init.f90`, `dynamics.f90`, and `hybrid.f90`.

### Default

	run 0 0.002