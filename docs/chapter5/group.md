## group

### Syntax

	group group_name style_cg style_at group_shape
	      x lower_b upper_b i j k
	      y lower_b upper_b i j k
	      z lower_b upper_b i j k
	      boolean_in group_axis
	      group_centroid_x group_centroid_y group_centroid_z
	      group_radius_large group_radius_small
	      boolean_move boolean_release boolean_def
	      vel vel_x vel_y vel_z
	      time time_start time_end
	      disp disp_lim
	      boolean_grad boolean_switch
	      grad_ref_axis grad_vel_axis
	      grad_ref_l grad_ref_u

* `group_name` = a string (length <= 30)

* `style_cg` = _element_ or _node_ or _null_

* `style_at` = _atom_ or _null_

* `group_shape` = _block_ or _cylinder_ or _cone_ or _tube_ or _sphere_

* `lower_b`, `upper_b` = real number or _inf_

* `i`, `j`, `k` = real number

* `boolean_in`, `boolean_move`, `boolean_release`, `boolean_def`, `boolean_grad`, `boolean_switch` = _t_ or _f_

		t is true
		f is false

* `group_axis`, `grad_ref_axis`, `grad_vel_axis` = _1_ or _2_ or _3_

* `group_centroid_x`, `group_centroid_y`, `group_centroid_z` = real number

* `group_radius_large`, `group_radius_small` = positive real number

* `vel_x`, `vel_y`, `vel_z` = real number

* `disp_lim` = non-negative real number

* `time_start`, `time_end` = non-negative integer

* `grad_ref_l`, `grad_ref_u` = real number or _inf_

### Examples

	group group_1 null atom block x inf inf 1. 0. 0. y inf inf 0. 1. 0. z 14.4 inf 0. 0. 1. t 3 20. 5. 0. 10. 10. f
	group group_2 node null cylinder x inf inf 1. 0. 0. y inf inf 0. 1. 0. z 14.4 inf 0. 0. 1. f 3 20. 5. 0. 10. 10. t t t vel 0. 0. 0. time 0 2500 disp 5. f
	group group_3 element atom cone x inf inf 1. 0. 0. y inf inf 0. 1. 0. z 14.4 inf 0. 0. 1. t 3 20. 5. 0. 10. 5. t t t vel 0. 0. 0. time 0 2500 disp 10. t f 2 1 50. 60.
	group group_4 element null sphere x inf inf 1. 0. 0. y inf inf 0. 1. 0. z 14.4 inf 0. 0. 1. t 3 20. 5. 0. 10. 10. t t t vel 0. 0. 0. time 0 2500 disp 3. t t 3 2 10. 100.
	group group_5 t t t vel 0. 0. 0. time 0 100 disp 3. f

### Description

This command sets controlled displacements for new groups and restart groups, the numbers of which are provided in the [group_num](group_num.md) command. The elements/nodes/atoms in a group are displaced at each simulation step (when `boolean_move` = _t_), deformed with the simulation cell deformation (when `boolean_def` = _t_), or not displaced/deformed. In any case, when the [`total_step`](run.md) is between `time_start` and `time_end`, the force on the group calculated by the [interatomic potential](potential.md) is discarded in `constraint.f90` and so does not take effect. The syntax, to some extent, is similar to the first one of the [modify](modify.md) command.

The new groups are created by first providing the elements/nodes/atoms information (by options from `style_cg` to `group_radius_small`) while the same information for the restart groups is read from `group_in_#.id`, where `#` is an positive integer starting from [`new_group_number`](group_num.md) + 1. The `group_in_#.id` files are renamed from the `group_out_#.id` files that were created automatically in previous CAC simulations when the total number of groups > 0.

For the restart groups, which are introduced when [`boolean_restart_group`](restart.md) = _t_ and [`restart_group_number`](group_num.md) > 0, the syntax of this command becomes (e.g., the fifth example)

	group group_name boolean_move boolean_release boolean_def
	      vel vel_x vel_y vel_z
	      time time_start time_end
	      disp disp_lim
	      boolean_grad boolean_switch
	      grad_ref_axis grad_vel_axis
	      grad_ref_l grad_ref_u

`style_cg` decides whether the group contains elements (_element_), nodes (_node_), or nothing (_null_) in the coarse-grained domain. [The differences between _element_ and _node_](../chapter8/element-node-diff.md) are also important in the [bd_group](bd_group.md) command. `style_at` decides whether the group contains atoms (_atom_) or nothing (_null_) in the atomistic domain.

There are currently five `group_shape`: _block_, _cylinder_, _cone_, _tube_, and _sphere_. The groups introduced in the [bd_group](bd_group.md) command has `group_shape` = _block_.

`lower_b` and `upper_b` are the lower and upper boundariess of the `group_shape`, respectively, in unit of the [lattice periodicity length](../chapter8/lattice-space.md), for the corresponding direction. When `lower_b` or `upper_b` is _inf_, the corresponding lower or upper simulation cell boundaries are taken as the `group_shape` boundaries, respectively.

`lower_b` and `upper_b` are their plane boundaries normal to the central axis `group_axis` direction. Note that `group_axis` is irrelevant when `group_shape` = _sphere_.

`i`, `j`, and `k` decide the `group_shape` (= _block_) boundary plane orientations with respect to the simulation cell, similar to those in the [box_dir](box_dir.md) command. When `modify_shape` = _cylinder_ or _cone_ or _tube_, they decide the direction of the `group_axis`, similar to those in the [modify](modify.md) commands.

Note that these five options (`lower_b`, `upper_b`, `i`, `j`, and `k`) are irrelevant when `group_shape` = _sphere_, and when `group_shape` = _cylinder_ or _cone_ or _tube_ if the corresponding direction is not `group_axis`. However, they need to be provided regardless.

When `boolean_in` = _t_, elements/nodes/atoms inside the `group_shape` belong to the group; otherwise, those outside do.

`group_centroid_x`, `group_centroid_y`, and `group_centroid_z`, in unit of the [maximum lattice periodicity length](../chapter8/lattice-space.md), are the coordinates of the center of the base plane of a _cylinder_ or _cone_ or _tube_, or the center of a _sphere_. When `group_shape` = _cylinder_ or _cone_ or _tube_, the `group_centroid_*` that corresponds to the `group_axis` becomes irrelevant. For example, when `group_axis` = _2_, `group_centroid_y` can take any real number without affecting the results.

`group_radius_large` is the base radius of a _cylinder_, the large base radius of a _cone_, the outer base radius of a _tube_, or the radius of a _sphere_. `group_radius_small`, the small base radius of a _cone_ or the inner base radius of a _tube_, is irrelevant for other `group_shape`. Both `group_radius_large` and `group_radius_small` are in unit of the [maximum lattice periodicity length](../chapter8/lattice-space.md).

Note that these six options (`group_axis`, `group_centroid_*`, and `group_radius_*`) are not relevant when `group_shape` = _block_. Yet, they need to be provided regardless.

When `boolean_move` = _t_, the group is assigned a displacement at each [simulation step](run.md); otherwise, no controlled displacement is applied and all following options become irrelevant, as in the first example. In the latter case, [the purpose of having a group](group_num.md) is to [calculate](cal.md) certain mechanical quantities of this group such as energy, force, and stress.

When `boolean_release` = _t_, the group is no longer assigned a displacement at each simulation step when [`total_step`](run.md) > `time_end`; otherwise, the group is assigned a zero displacment vector, i.e., fixed, when [`total_step`](run.md) > `time_end`.

When `boolean_def` = _t_, the group is deformed [along with the simulation box](deform.md), the same as that in the [bd_group](bd_group.md) command. Note that in both commands, the group is deformed only when [`total_step`](run.md) is between `time_start` and `time_end`. This option takes effect regardless of the controlled displacement vector. 

[`vel_x`, `vel_y`, `vel_z`] is the displacement vector assigned to the group at each simulation step, in unit of ps/Angstrom.

`time_start` and `time_end` are the starting and ending simulation steps, respectively, for the controlled displacement.

`disp_lim` is the upper bounds of the magnitude of the total group displacement, in unit of the [lattice constant](lattice.md). For example, if a group is displaced first by vector $$\mathbf{a}$$ then by vector $$\mathbf{b}$$ that is not parallel to $$\mathbf{a}$$, the total displacement is defined as $$|\mathbf{a}| + |\mathbf{b}|$$, instead of $$|\mathbf{a} + \mathbf{b}|$$. If the total displacement is larger than `disp_lim`, the displacement vector is zeroed.

When `boolean_grad` = _t_, the displacement is assigned to the group gradiently, i.e., different elements/nodes/atoms in the group may have different [`vel_x`, `vel_y`, `vel_z`]. The `grad_vel_axis` component of the displacement vector is linearly applied to the group based on the positions of elements/nodes/atoms along the `grad_ref_axis` direction. `grad_ref_l` and `grad_ref_u` are the lower and upper bounds of the graded displacement, in unit of the [lattice periodicity length](../chapter8/lattice-space.md), with _inf_ referring to the relevant simulation cell boundaries. The elements/nodes/atoms located at or below `grad_ref_l` are assigned a zero displacement, i.e., fixed; those located at or above `grad_ref_u` are assigned [`vel_x`, `vel_y`, `vel_z`]; those located between `grad_ref_l` and `grad_ref_u` are assigned a vector whose `grad_vel_axis` component is linearly graded while the other two components remain the same with respect to [`vel_x`, `vel_y`, `vel_z`].

In the third example, the elements/nodes/atoms which are located below $$50.0\times \mathrm{lattice\ periodicity\ length}$$ along the _y_ axis (because `grad_ref_axis` = _2_) are assigned a zero displacement vector; those located above $$60.0\times \mathrm{lattice\ periodicity\ length}$$ along the _y_ axis are assigned [`vel_x`, `vel_y`, `vel_z`]; those in between are assigned a linearly graded displacement vector whose _x_ component (because `grad_vel_axis` = _1_) is varied between zero and `vel_x` while its _y_ and _z_ components are `vel_y` and `vel_z`, respectively.

When `boolean_switch` = _t_, the lower and upper bounds of the graded displacement are switched. In the fourth example, the elements/nodes/atoms which are located below $$10.0\times \mathrm{lattice\ periodicity\ length}$$ along the _z_ axis (because `grad_ref_axis` = _3_) are assigned a displacement vector [`vel_x`, `vel_y`, `vel_z`]; those located above $$100.0\times \mathrm{lattice\ periodicity\ length}$$ along the _z_ axis are assigned a zero displacement; those in between are assigned a linearly graded displacement vector whose _y_ component (because `grad_vel_axis` = _2_) is varied between zero and `vel_y` while its _x_ and _z_ components are `vel_x` and `vel_z`, respectively.

### Related commands

There cannot be fewer `group` commands than [`new_group_number` + `restart_group_number`](group_num.md). When there are too many `group` commands in `cac.in`, those appearing later will be ignored. The `group_name` in the [cal](cal.md) command must match that in the current command.

The `group_name` of groups defined in the [bd_group](bd_group.md) command are group\_#, where # is an integer starting from `new_group_number` + `restart_group_number` + 1.

This command becomes irrelevant when [`new_group_number` + `restart_group_number`](group_num.md) = 0.

### Related files

`group.f90`

### Default

None.
