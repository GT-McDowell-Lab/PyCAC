## group

### Syntax

	group name_of_group style_cg style_at group_shape
	      x lower_b upper_b i j k
	      y lower_b upper_b i j k
	      z lower_b upper_b i j k
	      boolean_in group_axis
	      group_centroid_x group_centroid_y group_centroid_z
	      group_radius_large group_radius_small
	      boolean_move boolean_release boolean_def
	      vel vel_x vel_y vel_z
	      time time_start time_end
	      disp disp_l disp_u
	      boolean_grad boolean_switch
	      grad_ref_axis grad_vel_axis
	      grad_ref_l grad_ref_u

* name\_of\_group = a string with length <= 30

* style\_cg = _element_ or _node_ or _null_

* style\_at = _atom_ or _null_

* group\_shape = _block_ or _cylinder_ or _cone_ or _sphere_

* lower\_b, upper\_b = real number or _inf_

* i, j, k = real number

* boolean\_in, boolean\_move, boolean\_release, boolean\_def, boolean\_grad, boolean\_switch = _t_ or _f_

		t is true
		f is false

* group\_axis, grad\_ref\_axis, grad\_vel\_axis = _1_ or _2_ or _3_

* group\_centroid\_x, group\_centroid\_y, group\_centroid\_z, group\_radius\_large, group\_radius\_small = real number

* vel\_x, vel\_y, vel\_z, disp\_l, disp\_u, grad\_ref\_l, grad\_ref\_u = real number

* time\_start, time\_end = non-negative integer

### Examples

	group name_1 null atom block x inf inf 1. 0. 0. y inf inf 0. 1. 0. z 14.4 inf 0. 0. 1. t 3 20. 5. 0. 10. 10. f
	group name_2 node null cylinder x inf inf 1. 0. 0. y inf inf 0. 1. 0. z 14.4 inf 0. 0. 1. f 3 20. 5. 0. 10. 10. t t t vel 0. 0. 0. time 0 2500 disp 0. 100. f
	group name_3 element atom sphere x inf inf 1. 0. 0. y inf inf 0. 1. 0. z 14.4 inf 0. 0. 1. t 3 20. 5. 0. 10. 10. t t t vel 0. 0. 0. time 0 2500 disp 0. 100. t t 2 1 50. 60.

### Description

Set properties associated with a group.

The `name_of_group` could be any string with length smaller than or equal to 30.

`style_cg` and `style_at` decide whether the group contains elements, nodes, atoms, or null, see [here](ele_node_diff.md) for the differences between _element_ and _node_ in the coarse-grained domain.

There are currently four `group_shape` in PyCAC.

`lower_b` and `upper_b` are the boundaries of the group, in unit of the lattice periodic length along the corresponding axis. `i`, `j`, and `k` decides the group boundary plane orientation with respect to the simulation cell, in the same way as those in the [box](box.md) command. Note that these five quantities are relevant only when the `group_shape` is block.

When `boolean_in` is _t_, elements/nodes/atoms inside the `group_shape` belong to the group; otherwise, those outside the `group_shape` do.

`group_axis` is the central axis of the group; it is relevant only when the `group_shape` is _cylinder_ or _cone_.

`group_centroid_x`, `group_centroid_y`, and `group_centroid_z` are the coordinates of the center of the base plane of a _cylinder_ or _cone_, or the center of a _sphere_. For the _cylinder_ or _cone_, the `group_centroid` which corresponds to the `group_axis` becomes irrelevant.

`group_radius_large` and `group_radius_small` are the large and small radius of the group when the `group_shape` is _cylinder_ or _cone_ or _sphere_. The first quantity is relevant for all three `group_shape` while the second quantity is so only for the smaller base of the _cone_.

Note that the `group_axis`, `group_centroid`, and `group_radius` options are not relevant when the `group_shape` is _block_.

When `boolean_move` is _t_, the group is assigned a velocity, including the case that the velocity is zero; otherwise, there will be no constraints to the group and all following options become irrelevant. In any case, the group can be used for property calculations in the [cal](cal.md) command.

When `boolean_release` is _t_, the group is not assigned a velocity any more when the time step is larger than `time_end`.

When `boolean_def` is _t_, the group is deformed along with the simulation box, as set by the [deform](deform.md) command. This option is the same as that in the [bd_group](bd_group.md) command.

`vel_x`, `vel_y`, and `vel_z` are velocities assigned to the group along the _x_, _y_, and _z_ directions, respectively, in unit of distance unit/time unit. Please find the unit used in PyCAC [here](unit_pycac.md).

`time_start` and `time_end` are the starting and ending time step for the group deformation.

`disp_l` and `disp_u` are the lower and upper bounds of the group displacement, in unit of the lattice constant set by the [lattice](lattice.md) command.

When `boolean_grad` is _t_, the velocity is assigned to the group gradiently; otherwise the group velocity is applied uniformly and the following options become irrelevant.

When `boolean_switch` is _t_, the velocity at `grad_ref_u` is set as zero while that at `grad_ref_l` is at the maximum; otherwise, the velocity at `grad_ref_l` is set as zero. Note that `grad_ref_l` and `grad_ref_u` are the lower and upper bounds of the gradient, in unit of the lattice priodic length.

`grad_ref_axis` is the axis along which the gradient velocity is based on. For example, in the third example, `grad_ref_axis` = 2 and `boolean_switch` is true, then in this group, the elements/nodes/atoms which are located lower than 50. along the _y_ axis are assigned a velocity equalling the vector `vel_x` (because `grad_vel_axis` = 1); those located higher than 60. along the _y_ axis are assigned a zero velocity; those between 50. and 60. along the _y_ axis are assigned a linearly varying velocity between zero and `vel_x`, depending on their locations with respect to the 

### Related commands

The `name_of_group` in the [cal](cal.md) command must match that in the current command.

The `name_of_group` of groups defined in the [bd_group](bd_group.md) command are `name_#`, where `#` is an integer equallying `number_of_new_group` + `number_of_restart_group` + 1, 2, 3 ...

### Related files

`group.f90`

### Default

None.
