## group

### Syntax

	group group_name style_cg style_at group_shape
	      x lower_b upper_b i j k
	      y lower_b upper_b i j k
	      z lower_b upper_b i j k
	      boolean_in group_axis
	      group_centroid_x group_centroid_y group_centroid_z
	      group_radius_large group_radius_small

* `group_name` = a string (length <= 30)

* `style_cg` = _element_ or _node_ or _null_

* `style_at` = _atom_ or _null_

* `group_shape` = _block_ or _cylinder_ or _cone_ or _tube_ or _sphere_

* `lower_b`, `upper_b` = real number or _inf_

* `i`, `j`, `k` = real number

* `boolean_in` = _t_ or _f_

		t is true
		f is false

* `group_axis` = _1_ or _2_ or _3_

* `group_centroid_x`, `group_centroid_y`, `group_centroid_z` = real number

* `group_radius_large`, `group_radius_small` = positive real number

### Examples

	group group_1 null atom block x inf inf 1. 0. 0. y inf inf 0. 1. 0. z 14.4 inf 0. 0. 1. t 3 20. 5. 0. 10. 10.
	group group_2 node null cylinder x inf inf 1. 0. 0. y inf inf 0. 1. 0. z 14.4 inf 0. 0. 1. f 3 20. 5. 0. 10. 10.
	group group_3 element atom cone x inf inf 1. 0. 0. y inf inf 0. 1. 0. z 14.4 inf 0. 0. 1. t 3 20. 5. 0. 10. 5.
	group group_4 element null sphere x inf inf 1. 0. 0. y inf inf 0. 1. 0. z 14.4 inf 0. 0. 1. t 3 20. 5. 0. 10. 10.

### Description

This command sets new groups, the number of which is provided in the [group_num](group_num.md) command. The elements/nodes/atoms in a group, either a new group or a restar group, can be [moved](fix.md) at each [simulation step](run.md), [deformed with the simulation cell](deform.md) (when `boolean_def` in both [fix](fix.md) and [deform](deform.md) commands = _t_), or not moved/deformed. The syntax is similar to the first of that of the [modify](modify.md) command.

Different new groups cannot have the same `group_name`. Also, since the [restart groups](group_num.md) are automatically named `group_*`, where `*` is a positive integer starting from [`new_group_number`](group_num.md) + 1, the  `group_name` in this command cannot have any of those names.

`style_cg` decides whether the group contains elements (_element_), nodes (_node_), or nothing (_null_) in the coarse-grained domain; the differences between _element_ and _node_ are discussed [here](../chapter8/element-node-diff.md). `style_at` decides whether the group contains atoms (_atom_) or nothing (_null_) in the atomistic domain.

There are currently five `group_shape`: _block_, _cylinder_, _cone_, _tube_, and _sphere_.

`lower_b` and `upper_b` are the lower and upper boundaries of the `group_shape`, respectively, in units of the component of the [lattice periodicity length vector $$\vec{l'}_0$$](../chapter8/lattice-space.md) along the corresponding direction. When `lower_b` or `upper_b` = _inf_, the corresponding lower or upper simulation cell boundaries are taken as the `group_shape` boundaries, respectively. Note that when `group_shape` = _cylinder_ or _cone_ or _tube_, `lower_b` and `upper_b` are the lower and upper plane boundaries normal to the central axis `group_axis` direction, respectively.

`i`, `j`, and `k` decide the `group_shape` ($$\neq$$ _sphere_) boundary plane orientations with respect to the simulation cell, similar to those in the [box_dir](box_dir.md) command.

Note that these five options (`lower_b`, `upper_b`, `i`, `j`, and `k`) are irrelevant when `group_shape` = _sphere_, and when `group_shape` = _cylinder_ or _cone_ or _tube_ if the corresponding direction is not `group_axis`. Also, `group_axis` is irrelevant when `group_shape` = _block_ or _sphere_. However, they need to be provided regardless.

When `boolean_in` = _t_, elements/nodes/atoms inside the `group_shape` belong to the group; otherwise, those outside do.

`group_centroid_x`, `group_centroid_y`, and `group_centroid_z`, in units of the component of the [lattice periodicity length vector $$\vec{l'}_0$$](../chapter8/lattice-space.md) and with respect to the lower boundaries of the simulation cell along the corresponding direction, are the coordinates of the center of the base plane of a _cylinder_ or _cone_ or _tube_, or the center of a _sphere_. When `group_shape` = _cylinder_ or _cone_ or _tube_, the `group_centroid_*` that corresponds to the `group_axis` direction becomes irrelevant. For example, when `group_axis` = _2_, `group_centroid_y` can take any real number without affecting the results.

`group_radius_large` is the base radius of a _cylinder_, the large base radius of a _cone_, the outer base radius of a _tube_, or the radius of a _sphere_. `group_radius_small`, the small base radius of a _cone_ or the inner base radius of a _tube_, is irrelevant for other `group_shape`. Both `group_radius_large` and `group_radius_small` are in units of the [maximum lattice periodicity length $$l'_\mathrm{max}$$](../chapter8/lattice-space.md).

Note that these six options (`group_axis`, `group_centroid_*`, and `group_radius_*`) are not relevant when `group_shape` = _block_. Yet, they need to be provided regardless.

### Related commands

There cannot be fewer `group` commands than [`new_group_number`](group_num.md). When there are too many `group` commands, those appearing later will be ignored. The `group_name` in the [cal](cal.md) and [fix](fix.md) commands must match that in the current command.

This command becomes irrelevant when [`new_group_number`](group_num.md) = 0.

### Related files

`group.f90`, `fix_displacement.f90`, `fix_force.f90`, and `group_cal.f90`

### Default

None