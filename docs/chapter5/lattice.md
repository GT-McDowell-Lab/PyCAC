## lattice

### Syntax

	lattice chemical_element lattice_structure lattice_constant

* `chemical_element` = a string (length <= 30)

* `lattice_structure` = _fcc_ or _bcc_

* `lattice_constant` = positive real number

### Examples

	lattice Cu fcc 3.615
	lattice Al fcc 4.05
	lattice Fe bcc 2.8553

### Description

This command sets the lattice.

`lattice_constant` is in unit of Angstrom.

Note [that](../chapter1/pycac-feature.md) (i) the current PyCAC code can only simulate pure metals with single chemical element, (ii) `lattice_structure` must be either _fcc_ or _bcc_, yielding rhombohedral elements with {111} and {110} surfaces, respectively.

### Related commands

The atomic mass is provided in the [mass](mass.md) command.

`lattice_structure` becomes irrelevant when [`boolean_restart`](restart.md) = _t_, in which case there is no need for the lattice information.

### Related files

`box_init.f90` and `lattice.f90`

### Default

None.