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

When the style of a boundary is _p_, the corresponding [zigzag](zigzag.md) arg is changed to _f_. In other words, a boundary has to be flat to apply the periodic boundary condition.

### Related files

`ensemble.f90`

### Default

