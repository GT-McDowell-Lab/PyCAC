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

The command decides whether and how a force constraint is added to the system. When `boolean` is _t_, the equivalent nodal/atomic force vector is projected onto the [`ijk`] direction such that they can only move along that direction, either in dynamic or quasistatic CAC simulations.

Note that the direction is with respect to the simulation cell. For example, the second example projects the force vector onto the _z_ axis of the simulation cell.

### Related commands

None.

### Related files

`constraint.f90`

### Default

	constrain f 0. 0. 1.