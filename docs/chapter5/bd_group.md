## bd_group

### Syntax

	bd_group x boolean_l boolean_u style_cg style_at depth boolean_def time_start time_end
	         y boolean_l boolean_u style_cg style_at depth boolean_def time_start time_end
	         z boolean_l boolean_u style_cg style_at depth boolean_def time_start time_end

* `boolean_l`, `boolean_u`, `boolean_def` = _t_ or _f_

		t is true
		f is false
		
* `style_cg` = _null_ or _element_ or _node_

* `style_at` = _null_ or _atom_

* `depth` = postive real number

* `time_start`, `time_end` = non-negative integer

### Examples

	bd_group x f f null atom 2. t 200 1000 y t f node atom 3. t 0 1000 z t t element null 1. f 500 1000

### Description

This command provides a shortcut to create groups of elements/nodes/atoms that are within a certain distance from each simulation cell boundary (6 in total). The IDs of these groups follow the regular groups created or read (from `group_in_#.id`) by the [group](group.md) command. In groups created using this command, the elements/nodes/atoms are not displaced subject to the interatomic forces. In other words, equivalently in the [group](group.md) command,

* `boolean_move`, `boolean_release` = _t_

* `vel_x`, `vel_y`, `vel_z` = _0.0_

* `group_name` = group_# (where # is an integer starting from [`new_group_number` + `restart_group_number`](group.md) + 1)

Along a certain axis, `boolean_l` and `boolean_u` decide whether a group at the corresponding lower and upper boundaries is created, respectively, as illustrated in the figure below.

![bd-group](fig/bd-group.png)

If a group is to be created, `style_cg` and `style_at` become non-trivial. `style_cg` decides whether the group contains elements (_element_), nodes (_node_), or nothing (_null_) in the coarse-grained domain. [The differences between _element_ and _node_](../chapter8/element-node-diff.md) are also important in the [group](group.md) command. `style_at` decides whether the group contains atoms (_atom_) or nothing (_null_) in the atomistic domain.

All groups defined by this command have a block shape, i.e., as if `group_shape` = _block_ is set in the [group](group.md) command. Along the $$y$$ axis, for example, the groups at the lower and upper boundaries are respectively bounded by

	x inf inf y inf depth z inf inf
	x inf inf y upper_b-depth inf z inf inf

where `upper_b` is the upper boundary of the simulation cell, similar to that in the [group](group.md) command. The `depth` is in units of the component of the [lattice periodicity length vector $$\vec{l'}_0$$](../chapter8/lattice-space.md) along the corresponding axis.

`boolean_def` decides whether the group is [deformed along with the simulation cell](deform.md), the same as the one in the [group](group.md) command.

`time_start` and `time_end` are the [simulation steps](run.md) that decide when the groups begin to take effect and become unrestricted (i.e., `boolean_move` = _f_ in the [group](group.md) command), respectively.

### Related commands

Since this command provides a shortcut to create groups, all of its function can be realized by the [group](group.md) command.

### Related files

`group_init.f90`

### Default

None.
