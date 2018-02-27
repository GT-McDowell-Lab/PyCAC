## restart

### Syntax

	restart boolean_restart boolean_restart_refine

* `boolean_restart`, `boolean_restart_refine` = _t_ or _f_

		t is true
		f is false

### Examples

	restart f f
	restart t f
	restart t t

### Description

This command sets the restart styles.

When `boolean_restart` = _t_, the code reads the elements/nodes/atoms information from the `cac_in.restart` file; otherwise, the simulation cell is built from scratch and `boolean_restart_refine` becomes _f_ regardless of it value set in this command.

When `boolean_restart_refine` = _t_, all or some elements in the coarse-grained domain are [refined to atomic scale](http://dx.doi.org/10.1016/j.ijsolstr.2016.03.030) by linear interpolation from the nodal positions. Which elements to be refined depends on the [`refine_style`](refine.md).

### Related commands

When `boolean_restart_refine` = _f_, the [refine](refine.md) command becomes irrelevant, in which case there is no need for the refinement information.

### Related files

`read_restart.f90` and `write_restart.f90`

### Default

	restart f f