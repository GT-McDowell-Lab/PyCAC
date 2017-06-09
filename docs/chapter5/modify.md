## modify

### Syntax

	modify modify_name modify_style modify_shape
	       x lower_b upper_b i j k
	       y lower_b upper_b i j k
	       z lower_b upper_b i j k
	       boolean_in boolean_delete_filled modify_axis
	       modify_centroid_x modify_centroid_y modify_centroid_z
	       modify_radius_large modify_radius_small

	modify modify_name modify_style depth tolerance
			
* `modify_name` = a string (length <= 30)

* `modify_style` = _delete_ or _cg2at_ or _cutoff_

* `modify_shape` = _block_ or _cylinder_ or _cone_ or _tube_ or _sphere_

* `lower_b`, `upper_b` = real number or _inf_

* `i`, `j`, `k` = real number

* `boolean_in`, `boolean_delete_filled` = _t_ or _f_

		t is true
		f is false

* `modify_axis` = _1_ or _2_ or _3_

* `modify_centroid_x`, `modify_centroid_y`, `modify_centroid_z` = real number

* `modify_radius_large`, `modify_radius_small`, `depth`, `tolerance` = positive real number

### Examples

	modify modify_1 delete cylinder x 0. 1. 0.94281 0. -0.33333 y inf inf 0. 1. 0. z inf inf 0. 0. 1. t t 3 50. 50. 1. 2. 5.
	modify modify_2 cg2at block x inf inf 1. 0. 0. y 1. 12. 0. 0.94281 -0.33333 z inf inf 0. 0. 1. t f 1 20. 4. 5. 17. 13.
	modify modify_3 cutoff 0.1 0.01

### Description

This command sets the modifications made to the elements/nodes/atoms that are built from scratch, i.e., when [`boolean_restart`](restart.md) = _f_. The first syntax, to some extent, is similar to that of the [group](group.md) command for the new group.

There are currently three `modify_style`: _delete_, _cg2at_, and _cutoff_. When `modify_style` = _delete_ or _cg2at_, the first syntax is used; otherwise, the second syntax with _depth_ and _tolerance_ is used.

In the first syntax, there are five `modify_shape`: _block_, _cylinder_, _cone_, _tube_, and _sphere_. _delete_ removes some elements/atoms from the preliminary simulation cell, and _cg2at_ refines some elements into atomic scale.

`lower_b` and `upper_b` are the lower and upper boundaries of the `modify_shape`, respectively, in unit of the [lattice periodic length](../chapter8/lattice-space.md), for the corresponding direction. When `lower_b` or `upper_b` is _inf_, the corresponding lower or upper simulation cell boundaries are taken as the `modify_shape` boundaries, respectively.

`lower_b` and `upper_b` are their plane boundaries normal to the central axis `modify_axis` direction. Note that `modify_axis` is irrelevant when `modify_shape` = _sphere_.

`i`, `j`, and `k` decide the `modify_shape` boundary plane orientations with respect to the simulation cell, similar to those in the [box_dir](box_dir.md) and [group](group.md) commands.

Note that these five options (`lower_b`, `upper_b`, `i`, `j`, and `k`) are irrelevant when `modify_shape` = _sphere_, and when `modify_shape` = _cylinder_ or _cone_ or _tube_ if the corresponding direction is not `group_axis`. However, they need to be provided regardless.


When `boolean_in` = _t_, elements with any of their parts (in the coarse-grained domain) and atoms (in the atomistic domain) inside the `modify_shape` are deleted (_delete_) or refined to atomic scale (_cg2at_); otherwise, those outside are. In the coarse-grained domain, an element might have some part inside and the remaining part outside `modify_shape`; for this element, with _delete_, the region that is left behind due to the deletion may not have the shape specified by `modify_shape`. In this case, if `boolean_delete_filled` = _t_, atoms (that are linearly interpolated from the original element) will be filled in to maintain the `modify_shape`. E.g., if `boolean_in` = _t_, the interpolated atoms of the deleted elements that are outside `modify_shape` are filled in; otherwise, those inside are, as shown in the figure below. Note that `boolean_delete_filled` is irrelevant when `modify_style` = _cg2at_.

![modify](fig/modify.jpg)

`modify_centroid_x`, `modify_centroid_y`, and `modify_centroid_z`, in unit of the [lattice periodic length](../chapter8/lattice-space.md), are the coordinates of the center of the base plane of a _cylinder_ or _cone_ or _tube_, or the center of a _sphere_. When `modify_shape` = _cylinder_ or _cone_ or _tube_, the `modify_centroid_*` that corresponds to the `modify_axis` becomes irrelevant. For example, when `modify_axis` = _3_, `modify_centroid_z` can take any real number without affecting the results.

`modify_radius_large` is the base radius of a _cylinder_, the large base radius of a _cone_, the outer base radius of a _tube_, or the radius of a _sphere_. `modify_radius_small`, the small base radius of a _cone_ or the inner base radius of a _tube_, is irrelevant for other `group_shape`.

Note that these six options (`modify_axis`, `modify_centroid_*`, and `modify_radius_*`) are not relevant when `modify_shape` = _block_. Yet, they need to be provided regardless.

In the second syntax, which is for `modify_style` = _cutoff_, `depth` and `tolerance`, in unit of the [lattice periodic length](../chapter8/lattice-space.md) along the [grain stack direction](grain_dir.md), specify the size of the target region and the cutoff distance, respectively, as shown in the figure below.

![modify-cutoff](fig/modify-cutoff.jpg)

This is useful when the interatomic distance < `tolerance` or the distance between a node and an atom < `tolerance`, e.g., at the grain boundary, because of the [`overlap`](group_dir.md) or [grain origin displacements](grain_move.md). At first, a check is conducted, within the region set by `depth`, on both the real atoms in the atomistic domain or the interpolated atoms in the coarse-grained doain. Within a pair, if both are real atoms, the one associated with a smaller [`grain_id`](subdomain.md) is deleted; if one is a real atom and the other is an interpolated atom, the real atom is deleted; if both are interpolated atoms, an error message is issued because it is impossible to delete an interpolated atom from an element.

### Related commands

There cannot be fewer `modify` commands than [`modify_number`](modify_num.md). When there are too many `modify` commands in `cac.in`, those appearing later will be ignored.

This command becomes irrelevant when [`boolean_restart`](restart.md) = _t_ or [`modify_number`](modify_num.md) = 0.

### Related files

`model_modify.f90` and `model_modify_interpo.f90`

### Default

None.