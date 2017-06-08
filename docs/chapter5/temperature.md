## temperature

### Syntax

	temperature temp

* `temp` = positive real number

### Examples

	temperature 10.
	temperature 300.

### Description

This command sets the temperature for the [dynamic and hybrid](simulator.md) PyCAC simulations, in unit of K. In [quasi-static](minimize.md) simulations, the temperature is effectively 0.

### Related commands

A constant temperature is maintained in the system only when [`dyn_style`](dynamics.md) = _ld_. A warning will be issued if other `dyn_style` are used.

### Related files

`ensemble.f90`, `langevin_dynamics.f90`, and `langevin_vel.f90`

### Default

	temperature 10.