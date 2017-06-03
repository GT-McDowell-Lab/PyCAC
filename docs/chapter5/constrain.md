## constrain

### Syntax

	constrain boolean

* `boolean` = _t_ or _f_

		t is true
		f is faulse

### Examples

	constrain t

### Description

The command decides if a force constrain is added to the system. When `boolean` is _t_, the forces on the nodes and atoms are projected onto the direction specified by the [force_dir](force_dir.md) command such that they can only move along that direction, either in dynamic or quasi-static simulations.

### Related commands

[force_dir](force_dir.md)

### Related files

`constraint.f90`

### Default

`boolean` = f