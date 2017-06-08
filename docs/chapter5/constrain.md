## constrain

### Syntax

	constrain boolean i j k

* `boolean` = _t_ or _f_

		t is true
		f is faulse

* `i`, `j`, `k` = real number

### Examples

	constrain f 1. 1. 0.
	constrain t 0. 0. 1.

### Description

The command decides whether and how a force constrain is added to the system. When `boolean` is _t_, the nodal/atomic force vector is projected onto the [`i``j``k`] direction such that they can only move along that direction, either in dynamic or quasi-static simulations.

Note that the direction is with respect to the simulation cell. For example, the second example projects the force vector onto the _z_ axis of the simulation cell.

### Related commands

None.

### Related files

`constraint.f90`

### Default

	constrain f 0. 0. 1.