## mass

### Syntax

	mass atomic_mass

* `atomic_mass` = real number

### Examples

	mass 63.546
	mass 26.9815
	mass 58.6934
	mass 55.845

### Description

Set the mass of each atom, in unit of g/mol. The first, second, third, and fourth examples are for Cu, Al, Ni, and Fe, respectively. See [lattice](lattice.md) for chemical elements.

### Related commands

The mass matrix type is specified by the [mass_mat](mass_mat.md) command.

### Related files

`crystal.f90` and `mass_matrix.f90`, among many

### Default

None.