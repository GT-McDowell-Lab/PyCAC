## force_dir

### Syntax

	force_dir i j k

* `i`, `j`, `k` = real number

### Examples

	force_dir 1. 1. 0.
	force_dir 0. 0. 1.

### Description

This command projects the nodal/atomic force vector onto the [`i``j``k`] direction when `boolean` is true in the [constrain](constrain.md) command. Note that the direction is with respect to the simulation cell. For example, the second example projects the force vector onto the _z_ axis of the simulation cell.

### Related commands

This command is non-trivial only when `boolean` is true in the [constrain](constrain.md) command.

### Related files

`constraint.f90`

### Default

None.