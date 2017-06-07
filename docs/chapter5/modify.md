## modify

### Syntax

	modify modify_name modify_type modify_shape
	       x lower_b upper_b i j k
	       y lower_b upper_b i j k
	       z lower_b upper_b i j k
	       boolean_in boolean_delete_filled modify_axis
	       modify_centroid_x modify_centroid_y modify_centroid_z
	       modify_radius_large modify_radius_small

	modify modify_name modify_type depth tolerance
			
* modify_name = a string with length (<= 30)

* modify\_type = _delete_ or _cg2at_ or _cutoff_

* modify\_shape = _block_ or _cylinder_ or _cone_ or _tube_ or _sphere_

* lower\_b, upper\_b = real number or _inf_

* i, j, k = real number

* boolean\_in, boolean\_delete\_filled = _t_ or _f_

		t is true
		f is false

* modify\_axis = _1_ or _2_ or _3_

* modify\_centroid\_x, modify\_centroid\_y, modify\_centroid\_z, modify\_radius\_large, modify\_radius\_small = real number

* depth, tolerance = real number

### Examples

	modify name_1 delete cylinder x 0. 1. 0.94281 0. -0.33333 y inf inf 0. 1. 0. z inf inf 0. 0. 1. t t 3 50. 50. 1. 2. 5.
	modify name_2 cg2at block x inf inf 1. 0. 0. y 1. 12. 0. 0.94281 -0.33333 z inf inf 0. 0. 1. t f 1 20. 4. 5. 17. 13.
	modify name_3 cutoff 0.1 0.01

### Description

Set properties associated with a modification.

The `modify_name` could be any string with length smaller than or equal to 30.

There are currently three `modify_type`: _delete_, _cg2at_, and _cutoff_.

When the `modify_type` is _delete_ or _cg2at_, the first syntax is used; otherwise, the second syntax with _depth_ and _tolerance_ is used.

For _delete_ (remove elements/atoms) or _cg2at_ (refine elements into atomic scale), there are five `modify_shape`.

`lower_b` and `upper_b` are the boundaries of the group, in unit of the lattice periodic length along the corresponding axis. `i`, `j`, and `k` decides the group boundary plane orientation with respect to the simulation cell, in the same way as those in the box command. Note that these five quantities are relevant only when the `modify_shape` is _block_, as in the [group](group.md) command. 

When `boolean_in` is _t_, elements/nodes/atoms inside the `modify_shape` are deleted or refined to atoms; otherwise, those outside the `modify_shape` do. Note that in the coarse-grained domain, an element with any of its atoms inside or outside the `modify_shape` are deleted or refined to atoms.

For _delete_ only, after an element is deleted, sometimes part of the element is outside (when `boolean_in` = _t_) or inside (when `boolean_in` = _f_) the `modify_shape`. If `boolean_delete_filled` is _t_, this part of the element is refined into atomic scale; otherwise, no refinement takes place.

`modify_axis` is the central axis of the modification; it is relevant only when the `modify_shape` is _cylinder_ or _cone_ or _tube_.

`modify_centroid_x`, `modify_centroid_y`, and `modify_centroid_z` are the coordinates of the center of the base plane of a _cylinder_ or _cone_ or _tube_, or the center of a _sphere_. For the _cylinder_ or _cone_ or _tube_, the `modify_centroid` that corresponds to the `modify_axis` becomes irrelevant.

`modify_radius_large` and `modify_radius_small` are the large and small radius of the modification when the `modify_shape` is _cylinder_ or _cone_ or _tube_ or _sphere_. The first quantity is relevant for all three `modify_shape` while the second quantity is so only for the smaller base of the _cone_ and the inner radius of the _tube_.

Note that the `modify_axis`, `modify_centroid`, and `modify_radius` options are not relevant when the `modify_shape` is _block_.

`depth` and `tolerance` are relevant only when the `modify_type` is _cutoff_, which is used to delete one atom from a pair of atoms when the atomic distance is smaller than the `tolerance`. Both `depth` and `tolerance` are in unit the lattice periodic length. `depth` is the size of the cutoff region away from the grain boundary along the `grain_dir` direction as specified by the [grain_dir](grain_dir.md) command. Only the atoms, either the real atoms in the atomistic domain or the interpolated atoms in the coarse-grained doain, inside the cutoff region are checked for atomic cutoff. When both are real atoms, the one in the grain with a smaller `grain_id` is deleted; when one is a real atom and the other is an interpolated atom, the real atom is deleted; when both are interpolated atoms, an error will be issued because one cannot delete an interpolated atom from an element.

### Related commands

The number of modifications are set by the [modify_num](modify_num.md) command. Also, many options in this command are the same as those in the [group](group.md) command.

### Related files

`model_modify.f90`

### Default

None.