## bd_group

### Syntax

	bd_group x boolean_l boolean_u style_cg style_at depth boolean_def time_start time_end
	         y boolean_l boolean_u style_cg style_at depth boolean_def time_start time_end
	         z boolean_l boolean_u style_cg style_at depth boolean_def time_start time_end

* boolean\_l, boolean\_u, boolean\_def = _t_ or _f_

		t is true
		f is false
		
* style\_cg = _null_ or _element_ or _node_
* style\_at = _null_ or _atom_
* depth = real number
* time\_start, time\_end = an integer

### Examples

	bd_group x f f null atom 2. t 200 1000 y t f node atom 3. t 0 1000 z t t element null 1. f 500 1000

### Description

The `bd_group` command provides a shortcut to create groups for the elements/nodes/atoms within a certain distance from each boundary. The IDs of these groups are after the regular groups created by the [group](group.md) command. The groups created using this command are rigid, i.e., the elements/nodes/atoms are not displaced subject to the interatomic forces, expect (possibly) following the overall deformation of the simulation cell.

boolean\_l and boolean\_u decide whether the lower and upper boundaries along each axis are involved, respectively. If any of these two boolean is true, style\_cg and style\_at decide whether the group contains elements, nodes, atoms, or null, see [here](ele_node_diff.md) for the differences between _element_ and _node_.

All groups defined by the `bd_group` command have a block shape. Along the y axis, for example, the two block-shape groups are bounded by

	x inf inf y inf depth z inf inf
	x inf inf y upper_b-depth inf z inf inf

where upper\_b is the upper bound of the simulation cell, similar to that in the [group](group.md) command. Note that the depth must be a real number, e.g., `2.`, instead of an integer, e.g., `2`. The depth is in unit of the [lattice\_space\_max](this is the maximum periodic lattice spacing in the system) along respective axis.

boolean\_def decides whether the group is deformed along with the simulation cell, similar to the one in the [group](group.md) command.

time\_start and time\_end, in the unit of time step, are two integers of when the groups begin and stop being rigid.

### Related commands

This command provides a shortcut to create groups, which can be done by the [group](group.md) command.

### Related files

`group_init.f90`

### Default

None.
