## shared elements

One issue that does not exist in parallel atomistic simulations but requires special attention in par- allel finite element implementations is that in the latter some elements may be shared between neighboring processors. In CAC, this issue originates from the difference in shape between the parallelepipedonal processor domain and the rhombohedral finite elements with arbitrary crystallographic orientations, the latter of which also results in the [jagged simulation cell boundaries](../chapter5/zigzag.md). Instead of having all relevant processors calculate the same quantities (e.g., force, energy, and virial) within a shared element, in the PyCAC code, each relevant processor only calculates quantities of the integration points its domain contains. Then these quantities are summed in the `processor_equiv.f90` subroutine, after which all relevant processors have the same nodal quantities. This simple summation is feasible because of the trilinear shape function employed in the finite elements.

To facilitate the shared element-related calculations, a public array `tag_shared_ele` and a public variable `ele_shared_num` are introduced. For example, processor 3 has 6 local elements, with the 2nd, 4th, and 5th elements shared with other processors, then

	tag_ele_shared(1) = 0
	tag_ele_shared(2) = 1
	tag_ele_shared(3) = 0
	tag_ele_shared(4) = 2
	tag_ele_shared(5) = 3
	tag_ele_shared(6) = 0

and

	ele_shared_num = 3

The array and the variable, defined in `processor_scatter_cg.f90` and updated in `update_neighbor_cg.f90`, are used in these three subroutines: `processor_edenshost_intpo.f90`, `processor_equiv.f90`, and `processor_langevin_cg.f90`.

Note that in current PyCAC code, the "shared element communication" process mentioned above does NOT involve a host processor as described in page 123 of [Xu et al.](http://dx.doi.org/10.1016/j.ijplas.2015.05.007), which was for a previous version. The host processor, which has the highest rank among all processors that share the same element, is indeed used in the code, but only for the purposes of (i) sending the element/node information to the [root processor](rank.md) for output, e.g., in `all_to_one_cg.f90` and `all_to_one_group_cg.f90`, and (ii) calculating certain variables based on the global arrays, e.g., the global force norm `force_norm` calculated in `conjugate_gradient.f90`, `fire.f90`, `langevin_vel.f90`, `quenched_vel.f90`, `quick_mini.f90`, `steepest_descent.f90`, and `update_vel.f90`. For example, when processor 2 and processor 3 share the same element (and thus have the same relevant nodal information), only one of them needs to send the information to root. The host processor is set in the `processor_scatter_cg.f90` subroutine, in which the array `who_has_ele(ie) = .true.` for the host processor and `.false.` for non-host processors, where `ie` is the local element id.


