## temperature

### Syntax

	temperature temp

* `temp` = positive real number

### Examples

	temperature 10.
	temperature 300.

### Description

This command sets the temperature for the [dynamic and hybrid](simulator.md) CAC simulations, in unit of K. In [quasi-static](minimize.md) simulations, the temperature is effectively 0 K.

### Related commands

A constant temperature is maintained in the system only when [`dyn_style`](dynamics.md) = _ld_. The user will get a warning message if other [`dyn_style`](dynamics.md) are used.

### Related files

`ensemble.f90`, `langevin_dynamics.f90`, and `langevin_vel.f90`

### Default

	temperature 10.