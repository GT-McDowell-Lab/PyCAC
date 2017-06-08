## mass_mat

### Syntax

	mass_mat mass_matrix

* `mass_matrix` = _lumped_ or _consistent_

### Examples

	mass_mat lumped
	mass_mat consistent

### Description

This command sets the mass matrix type used in the finite element calculation. The lumped mass matrix approximates the mass of each element and distributes it to the nodes. The consistent mass matrix distributes the exact mass over the entire element. 

### Related commands

The atomic mass is defined by the [mass](mass.md) command.

### Related files

`mass_matrix.f90` and `update_equiv.f90`

### Default

	mass_mat lumped