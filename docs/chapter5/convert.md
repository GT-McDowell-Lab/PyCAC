## convert

### Syntax

	convert i j k

* `i`, `j`, `k` = real number

### Examples

	convert -1. 1. 2.
	convert 1. -1. 0.

### Description

This command converts the crystallographic orientation [`i``j``k`] of each grain to the orientation with respect to the simulation cell [`i'``j'``k'`]. Results of this conversion will be shown on the screen as

	Converted box direction of grain # is i' j' k'

where the positive integer `#` is the grain ID.

For example, if the lattice orientation of the second grain along the _x_ axis is [211], this command will convert the [211] crystallographic orientation into [100] and output

 	Converted box direction of grain 2 is 1.0000 0.0000 0.0000

### Related commands

This command is useful when the user has a set of crystallographic orientations in mind and wants to find the orientation with respect to the simulation cell, e.g., to be used in the [box_dir](box_dir.md) command.

### Related files

`convert_direction.f90`

### Default

	convert 0. 0. 0.