## element

### Syntax

	element mass_matrix intpo_depth

* `mass_matrix` = _lumped_ or _consistent_

* `intpo_depth` = _1_ or _2_

### Examples

	element lumped 2
	element consistent 1

### Description

This command sets the element type used in the finite element calculation in the coarse-grained domain.

For `mass_matrix`, the _lumped_ type approximates the mass of each element and distributes it to the nodes; the _consistent_ type distributes the exact mass over the entire element.

`intpo_depth` decides whether the first nearest neighbor (1NN) or the second nearest neighbor (2NN) elements are employed in the coarse-grained domain; their differences are illustrated in Fig. B26 of [Xu et al., 2015](http://dx.doi.org/10.1016/j.ijplas.2015.05.007).

### Related commands

The atomic mass is provided in the [mass](mass.md) command.

### Related files

`mass_matrix.f90`, `integration_point.f90`, and `update_equiv.f90`

### Default

	element lumped 2