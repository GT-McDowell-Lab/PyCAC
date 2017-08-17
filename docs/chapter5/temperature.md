## temperature

### Syntax

	temperature temp

* `temp` = non-negative real number

### Examples

	temperature 10.
	temperature 300.

### Description

This command sets the temperature for the [dynamic and hybrid](simulator.md) CAC simulations in K. A constant finite temperature is maintained in the system only when [`dyn_style`](dynamics.md) = _ld_, i.e., Langevin dynamics. When `temp` = 0, [the equation of motion for the Langevin dynamics reduces to that for the damped dynamics](dynamics.md).

In [quasi-static](minimize.md) simulations, the temperature is effectively 0 K.

### Related commands

The temperature becomes irrelevant if other [`dyn_style`](dynamics.md) are used, and the user will get a warning message.

### Related files

`ensemble.f90`, `langevin_dynamics.f90`, and `langevin_vel.f90`

### Default

	temperature 10.
