## temperature

### Syntax

	temperature temp

* temp = real number

### Examples

	temperature 10.
	temperature 300.

### Description

Set the temperature for the dynamic and hybrid PyCAC simulations, in unit of K.

### Related commands

Only the _ld_ type in the [dynamics](dynamics.md) command can keep a constant temperature in the system.

### Related files

`ensemble.f90`, `langevin_dynamics.f90`, and `langevin_vel.f90`

### Default

	temperature 10.