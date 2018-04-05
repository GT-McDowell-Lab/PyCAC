## modify

### Syntax

	modify modify_name modify_style modify_shape
	       x lower_b upper_b i j k
	       y lower_b upper_b i j k
	       z lower_b upper_b i j k
	       boolean_in boolean_delete_filled modify_axis
	       modify_centroid_x modify_centroid_y modify_centroid_z
	       modify_radius_large modify_radius_small

	modify modify_name modify_style line_axis plane_axis
	       modify_centroid_x modify_centroid_y modify_centroid_z
	       dis_angle poisson_ratio

	modify modify_name modify_style depth tolerance

	modify modify_name modify_style disp_x disp_y disp_z
			
* `modify_name` = a string (length <= 30)

* `modify_style` = _delete_ or _cg2at_ or _dislocation_ or _cutoff_ or _add\_atom_

* `modify_shape` = _block_ or _cylinder_ or _cone_ or _tube_ or _sphere_

* `lower_b`, `upper_b` = real number or _inf_

* `i`, `j`, `k` = real number

* `boolean_in`, `boolean_delete_filled` = _t_ or _f_

		t is true
		f is false

* `modify_axis`, `line_axis`, `plane_axis` = _1_ or _2_ or _3_

* `modify_centroid_x`, `modify_centroid_y`, `modify_centroid_z`, `dis_angle`, `poisson_ratio`, `add_x`, `add_y`, `add_z` = real number

* `modify_radius_large`, `modify_radius_small`, `depth`, `tolerance` = positive real number

### Examples

	modify del_sth delete cylinder x 0. 1. 0.94281 0. -0.33333 y inf inf 0. 1. 0. z inf inf 0. 0. 1. t t 3 50. 50. 1. 2. 5.
	modify refine_sth cg2at block x inf inf 1. 0. 0. y 1. 12. 0. 0.94281 -0.33333 z inf inf 0. 0. 1. t f 1 20. 4. 5. 17. 13.
	modify create_dis dislocation 1 3 1. 20. 3.2 60. 0.36
	modify use_cutoff cutoff 0.1 0.01
	modify add_some_atoms add_atom 1. 3. 2.

### Description

This command sets the modifications made to the elements/nodes/atoms that are built from scratch, i.e., when [`boolean_restart`](restart.md) = _f_. The first syntax is similar to that of the [group](group.md) command.

There are currently five `modify_style`: _delete_, _cg2at_, _dislocation_, _cutoff_, and _add\_atom_. When `modify_style` = _delete_ or _cg2at_, the first syntax is used; when `modify_style` = _dislocation_, the second syntax is used; when `modify_style` = _cutoff_, the third syntax is used; otherwise, the fourth syntax is used.

#### First syntax (`modify_style` = _delete_ or _cg2at_)

The first syntax removes some elements/atoms (_delete_) or refines some elements into atomic scale (_cg2at_), based on the simulation cell built from scratch.

There are five `modify_shape`: _block_, _cylinder_, _cone_, _tube_, and _sphere_.

`lower_b` and `upper_b` are the lower and upper boundaries of the `modify_shape`, respectively, in units of the component of the [lattice periodicity length vector $$\vec{l'}_0$$](../chapter8/lattice-space.md) along the corresponding direction. When `lower_b` or `upper_b` = _inf_, the corresponding lower or upper simulation cell boundaries are taken as the `modify_shape` boundaries, respectively. Note that when `modify_shape` = _cylinder_ or _cone_ or _tube_, `lower_b` and `upper_b` are the lower and upper plane boundaries normal to the central axis `modify_axis` direction, respectively.

`i`, `j`, and `k` decide the `modify_shape` ($$\neq$$ _sphere_) boundary plane orientations with respect to the simulation cell, similar to those in the [box_dir](box_dir.md) command.

Note that these five options (`lower_b`, `upper_b`, `i`, `j`, and `k`) are irrelevant when `modify_shape` = _sphere_, and when `modify_shape` = _cylinder_ or _cone_ or _tube_ if the corresponding direction is not `modify_axis`. Also, `modify_axis` is irrelevant when `modify_shape` = _block_ or _sphere_. However, they need to be provided regardless.

When `boolean_in` = _t_, elements with any of their parts (in the coarse-grained domain) and atoms (in the atomistic domain) inside the `modify_shape` are deleted (_delete_) or [refined to atomic scale](http://dx.doi.org/10.1016/j.ijsolstr.2016.03.030) (_cg2at_); otherwise, those outside are. In the coarse-grained domain, an element might have some part  of it inside and the remaining part outside `modify_shape`; for this element, with _delete_, the region that is left behind due to the deletion may not have the shape specified by `modify_shape`. In this case, if `boolean_delete_filled` = _t_, atoms (that are linearly interpolated from the original element) will be filled in to maintain the `modify_shape`. E.g., if `boolean_in` = _t_, the interpolated atoms of the deleted elements that are outside `modify_shape` are filled in; otherwise, those inside are, as shown in the figure below. Note that `boolean_delete_filled` is irrelevant when `modify_style` = _cg2at_.

![modify](fig/modify.png)

Also note that while _delete_ applies to both atomistic and coarse-grained domains, _cg2at_ applied to the coarse-grained domain only. Different from the [group](group.md) command in which the user should pay attention to [the difference between _element_ and _node_](../chapter8/element-node-diff.md), a modification follows one simple rule in the coarse-grained domain: an element and all its nodes are selected if any interpolated atom of this element is inside (if `boolean_in` = _t_) or outside (if `boolean_in` = _f_) `modify_shape`.

`modify_centroid_x`, `modify_centroid_y`, and `modify_centroid_z`, in units of the component of the [lattice periodicity length vector $$\vec{l'}_0$$](../chapter8/lattice-space.md) and with respect to the lower boundaries of the simulation cell along the corresponding direction, are the coordinates of the center of the base plane of a _cylinder_ or _cone_ or _tube_, or the center of a _sphere_. When `modify_shape` = _cylinder_ or _cone_ or _tube_, the `modify_centroid_*` that corresponds to the `modify_axis` becomes irrelevant. For example, when `modify_axis` = _3_, `modify_centroid_z` can take any real number without affecting the results.

`modify_radius_large` is the base radius of a _cylinder_, the large base radius of a _cone_, the outer base radius of a _tube_, or the radius of a _sphere_. `modify_radius_small`, the small base radius of a _cone_ or the inner base radius of a _tube_, is irrelevant for other `modify_shape`. Both `modify_radius_large` and `modify_radius_small` are in units of the [maximum lattice periodicity length $$l'_\mathrm{max}$$](../chapter8/lattice-space.md).

Note that these six options (`modify_axis`, `modify_centroid_*`, and `modify_radius_*`) are not relevant when `modify_shape` = _block_. Yet, they need to be provided regardless.

#### Second syntax (`modify_style` = _dislocation_)

The second syntax builds a full dislocation into the simulation cell, with nodes/atoms displaced following the isotropic displacement field. In [FCC and BCC lattices](lattice.md), a full dislocation has a Burgers vector magnitude of $$(\sqrt{2}/2)a_0$$ and $$(\sqrt{3}/2)a_0$$, respectively, where $$a_0$$ is the [`lattice_constant`](lattice.md). Multiple `modify` commands with `modify_style` = _dislocation_ can be employed to introduce multiple dislocations.

`line_axis` and `plane_axis` are the dislocation line axis and the plane normal axis, respectively. They cannot be the same.

`modify_centroid_x`, `modify_centroid_y`, and `modify_centroid_z`, in units of the component of the [lattice periodicity length vector $$\vec{l'}_0$$](../chapter8/lattice-space.md) and with respect to the lower boundaries of the simulation cell along the corresponding direction, are the coordinates of the origin with respect to which the displacement field is built. For example, if one wants to build a dislocation passing through the centroid of the simulation cell, these three quantities should be at the centroid. Note that in the coarse-grained and atomistic domains, the slip plane, which contains the dislocation along `line_axis` and has a normal direction `plane_axis`, should be located between two adjacent elements and two atomic layers, respectively.

`dis_angle` and `poisson_ratio` are the dislcoation character angle (in degrees) and the isotropic Poisson's ratio of the material, respectively.

#### Third syntax (`modify_style` = _cutoff_)

The third syntax deletes one atom from a pair of atoms (either real atoms in the atomistic domain or interpolated atoms in the coarse-grained domain) when they are too close, at the grain boundary. The situation that some atoms are too close to each other is usually a result of the [`overlap`](group_dir.md) or [grain origin displacements](grain_move.md). Among all `modify` commands, there should be no more than one with `modify_style` = _cutoff_.

`depth` and `tolerance`, in units of the component of the [lattice periodicity length vector $$\vec{l'}_0$$](../chapter8/lattice-space.md) along the [grain stack direction](grain_dir.md), specify the size of the target region and the cutoff distance, respectively, as shown in the figure below. In most cases, `tolerance` should not be larger than or equal to the first nearest neighbor distance in a perfect lattice.

![modify-cutoff](fig/cutoff.png)

At each grain boundary, a check is first conducted, within the region set by `depth` along the [grain stack direction](grain_dir.md), on both the real atoms in the atomistic domain or the interpolated atoms in the coarse-grained doain. In the figure above, (i) all atoms in the red shaded region (grain I) will be run against those in the left green shaded region (grain II), (ii) all atoms in the right green shaded region (grain II) will be run against those in the blue shaded region (grain III). Within a pair, if both are real atoms, the one associated with a smaller [`grain_id`](subdomain.md) is deleted; if one is a real atom and the other is an interpolated atom, the real atom is deleted; if both are interpolated atoms, the user will get an error message because it is impossible to delete a single interpolated atom from an element, which would violate the hyperelastic body assumption of an element.

#### Fourth syntax (`modify_style` = _add\_atom_)

The fourth syntax adds additional atoms to the simulation cell built from scratch. It cannot add additional elements. The information of the atoms to be added is read from [LAMMPS data files](http://lammps.sandia.gov/doc/2001/data_format.html) `lmp_*.dat`, where `*` is the id of the current modify command in `cac.in`. For example, if the commands look like this:

	modify del_sth delete cylinder x 0. 1. 0.94281 0. -0.33333 y inf inf 0. 1. 0. z inf inf 0. 0. 1. t t 3 50. 50. 1. 2. 5.
	modify add_first add_atom 1. 3. 2.
	modify create_dis dislocation 1 3 1. 20. 3.2 60. 0.36
	modify add_second add_atom -1. 4. 2.

then two files, naming, `lmp_2.dat` and `lmp_4.dat` should be provided.

`disp_x`, `disp_y`, and `disp_z`, in units of the component of the [lattice periodicity length vector $$\vec{l'}_0$$](../chapter8/lattice-space.md) and with respect to the lower boundaries of the simulation cell along the corresponding direction, are the displacement of the added atoms with respect to their original positions in `lmp_*.dat`. If `disp_x`, `disp_y`, and `disp_z` are all zero, the atoms are added as is.

This `modify_style` can be useful in constructing models containing grain boundaries (GBs). For example, the GB region (which may not have energy minimized GB structures) of a bicrystal model may be deleted first, before the energy minimized GB structures presented in [LAMMPS data files](https://materialsdata.nist.gov/handle/11256/358) are added to the model. This can be realized by first using a modify command with `modify_style` = _delete_, followed by another modify command with `modify_style` = _add\_atom_. 

### Related commands

There cannot be fewer `modify` commands than [`modify_number`](modify_num.md). When there are too many `modify` commands in `cac.in`, those appearing later will be ignored.

This command becomes irrelevant when [`boolean_restart`](restart.md) = _t_ or [`modify_number`](modify_num.md) = 0, in which case there is no need for the modification information.

### Related files

`model_modify.f90`, `model_modify_interpo.f90`, `model_add_atom.f90`, `model_cutoff.f90`, `model_cutoff_bd.f90`, `model_dislocation.f90`, `model_cg2at.f90`, `model_delete.f90`, and `model_rearrange.f90`.

### Default

None.

### Acknowledgements

[Rigelesaiyin Ji](https://www.aere.iastate.edu/lmxiong/people-2/) and [Jaber R. Mianroodi](https://scholar.google.com/citations?user=m18d-jwAAAAJ&hl=en) are acknowledged for helpful discussions in implementing the second syntax.