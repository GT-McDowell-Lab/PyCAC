## constrain

### Syntax

	constrain boolean

* boolean = _t_ or _f_

		t is true
		f is faulse

### Examples

	constrain t

### Description

Decide if a constrain is added to the system. When `boolean` is _t_, the nodes and atoms are only allowed to move along the direction specified by the [force_dir](force_dir.md) command, either in dynamic or quasi-static simulations.

### Related commands

[force_dir](force_dir.md)

### Related files

`constraint.f90`

### Default

`boolean` = f