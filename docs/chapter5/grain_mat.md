## grain_mat

### Syntax

	grain_mat {grain_id x i j k y i j k z i j k}

* i, j, k = real number

### Examples

	grain_mat 1 x -1. 1. -2. y 1. 1. 0. z 1. -1. -1.
	grain_mat 1 x 1. 1. 0. y -1. 1. 2. z 1. -1. 1. 2 x 1. 1. 0. y -1. 1. -2. z -1. 1. 1.

### Description

Set the lattice orientation in each grain, along the _x_, _y_, and _z_ directions, respectively. Any two sets of vector must be normal to each other. The right hand rule must be obeyed, e.g., the cross product between the vector for the _x_ axis cross and that for the _y_ axis must be along the _z_ axis. An error will be issued if any of these rules is broken.


### Related commands

The number of grain is specified by the [grain_num](grain_num.md) command.

### Related files

`grain.f90`

### Default

	grain_mat 1 x 1. 0. 0. y 0. 1. 0. z 0. 0. 1.