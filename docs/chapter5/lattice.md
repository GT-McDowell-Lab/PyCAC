## lattice

### Syntax

	lattice chemical_element lattice_structure lattice_constant

* chemical\_element = a string with length <= 30

* lattice\_structure = _fcc_ or _bcc_

* lattice\_constant = real number

### Examples

	lattice Cu fcc 3.615
	lattice Al fcc 4.05
	lattice Fe bcc 2.8553

### Description

Set the lattice used in PyCAC simulation. Note that currently, the PyCAC code only accepts pure metals with single chemical element.

`chemical_element` can be any.

`lattice_structure` must be either _fcc_ or _bcc_. An error will be issued if other lattice structures are provided.

`lattice_constant` is in unit of Angstrom.

### Related commands

The mass of each atom in the lattice is defined by the [mass](mass.md) command.

### Related files

`box_init.f90` and `lattice.f90`

### Default

None.