## force_dir

### Syntax

	force_dir i j k

* i, j, k = real number

### Examples

	force_dir 1. 1. 0.
	force_dir 0. 0. 1.

### Description

Project the force vector onto the direction of `force_dir` when `constrain` is true as specified by the [constrain](constrain.md) command. Note that the direction is with respect to the simulation cell: the second example points to the _z_ axis.

### Related commands

This command is relevant only when `constrain` is true as specified by the [constrain](constrain.md) command.

### Related files

`constraint.f90`

### Default

	force_dir 0. 0. 1.