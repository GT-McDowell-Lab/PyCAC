## restart

### Syntax

	restart boolean_restart boolean_restart_refine boolean_restart_group

* `boolean_restart`, `boolean_restart_refine`, `boolean_restart_group` = _t_ or _f_

		t is true
		f is false

### Examples

	restart f f f
	restart t f f
	restart t t f

### Description

This command sets the restart styles.

When `boolean_restart` = _t_, the code reads the elements/nodes/atoms information from the `cac_in.restart` file; otherwise, the simulation cell is built from scratch and both `boolean_restart_refine` and `boolean_restart_group` become _f_ regardless of their values in this command.

When `boolean_restart_refine` = _t_, all or some elements in the coarse-grained domain are [refined to atomic scale](http://dx.doi.org/10.1016/j.ijsolstr.2016.03.030) by linear interpolation from the nodal positions. Which elements to be refined depends on the [`refine_style`](refine.md).

When `boolean_restart_group` = _t_, elements/nodes/atoms information of the [restart group](group_num.md) is read from `group_in_#.id` files, where `#` is an positive integer starting from [`new_group_number`](group_num.md) + 1. On the one hand, there cannot be fewer `group_in_#.id` files than [`restart_group_number`](group_num.md); on the other hand, any `group_in_#.id` file with `#` > [`new_group_number` + `restart_group_number`](group_num.md) is ignored by this command. When `boolean_restart_group` = _f_, [`restart_group_number`](group_num.md) becomes 0, regardless of its value in the [group_num](group_num.md) command.

### Related commands

When `boolean_restart_refine` = _f_, the [refine](refine.md) command becomes irrelevant, in which case there is no need for the refinement information.

When `boolean_restart_group` = _t_, the [group_num](group_num.md) and [fix](fix.md) commands provide the restart group number and the displacement/force information, respectively.

### Related files

`read_restart.f90` and `write_restart.f90`

### Default

	restart f f f
