## mass

### Syntax

	mass atomic_mass

* `atomic_mass` = positive real number

### Examples

	mass 63.546
	mass 26.9815
	mass 55.845

### Description

This command sets the atomic mass, in unit of g/mol. The three examples are for Cu, Al, and Fe, respectively, corresponding to those in the [lattice](lattice.md) command. Note the current PyCAC code can only simulate [pure metals](../chapter1/pycac-feature.md).

### Related commands

The mass matrix type in the finite element calculation in the coarse-grained domain is specified in the [mass_mat](mass_mat.md) command.

### Related files

`crystal.f90` and `mass_matrix.f90`

### Default

None.