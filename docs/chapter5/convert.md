## convert

### Syntax

	convert i j k

* i,j,k = real number

### Examples

	convert -1. 1. 2.
	convert 1. -1. 0.

### Description

Convert the lattice orientation [i,j,k] to the orientation with respect to the simulation cell.


### Related commands

This command is useful when the user has a set of lattice orientations in mind and wants to find the orientation with respect to the simulation cell, e.g., to be used in the [box](box.md) command.

### Related files

`convert_direction.f90`

### Default

None.