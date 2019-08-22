
### atom

There are some arrays with `atom` in their names, e.g., `r_atom`, `vel_atom`, `force_atom`, which respectively are the positions, velocities, and forces of real atoms in the atomistic domain. On the other hand, defined in `atom_para_module.f90`, there are `atom_num_l`, which is the number of local atoms in each processor domain, `atom_num_lg`, which is the number of local AND ghost atoms in each processor domain, and `atom_num_lr`, which is the actual size of the second dimension of some `atom`-related arrays. The differences between `atom_num_l`, `atom_num_lg`, and `atom_num_lr`, as well as their relation with some `atom`-related arrays are explained below.

Say that the system contains 100 atoms using three processors, then either `read_restart.f90` (if one restarts a previous simulation) or `model_assemble.f90` (if one builds the model from scratch), set by [`boolean_restart`](../chapter-5/restart.md), will first calculate `atom_num_l` as

	atom_num_l = nint((real(atom_num, wp) / pro_num) * 1.2_wp)

In our case, `atom_num_l` = 40, following which most `atom`-related arrays are allocated.

Next, in `processor_scatter_atomistic.f90`, one first lets `atom_num_lr` equal `atom_num_l`, then the root processor distributes all atoms to all processors (including root itself); if the actual number of local atoms one processor should have is larger than `atom_num_lr`, `atom_num_lr` is increased by `seg_num` which is 1024 as set in `module/cac_para_module.f90`. In the meantime, many `atom`-related arrays also increase their size. Assume that the root processor should contain 50 local atoms while the other two processors 25 each, `atom_num_lr` becomes 40 + 1024 = 1064 for root but still 40 for the other two processors. At the end of this subroutine, some `atom`-related arrays, e.g., `r_atom`, have a size of 3 by 1064 for root while 3 by 40 for the other two processors; `atom_num_l`, which is expected to be the number of local atoms for each processor, is re-calculated to be 50 for root and 25 for the other two processors.

Next, in `processor_ghost_atomistic.f90`, the ghost atoms are added to the end of some `atom`-related arrays. Again, if the number of local+ghost atoms is larger than `atom_num_lr`, `atom_num_lr` is further increased by `seg_num`, along with the expansion in size of some `atom`-related arrays. Assume that the numbers of ghost atoms are 30, 10, and 20 for the three processors, respectively, `atom_num_lr` would be 1064 for root (because 50 + 30 < 1064), 40 for processor 1 (because 25 + 10 < 40), and 1064 for processor 2 (because 25 + 20 > 40). In other words, `atom_num_lr` increases for the last processor while remaining the same for the other two processors. At the end of this subroutine, `atom_num_lg` is assigned as the actual number of local + ghost atoms, i.e., 80, 35, and 45 for the three processors, respectively.

In sum, `atom_num_l` <= `atom_num_lg` <= `atom_num_lr`. Note that (i) `atom_num` is the total number of real atoms in the system, i.e., 100, regardless of how many processors are involved and how many ghost atoms are needed; (ii) in the case of single processor, there may still be ghost atoms if [periodic boundary conditions](../chapter-5/boundary.md) are used.

### atomap

There are also some arrays with `atomap` in their names, e.g., `r_atomap`, which is the positions of interpolated atoms in the coarse-grained domain. On the other hand, defined in `interpo_para_module.f90`, there are `atomap_num_l`, which is the number of interpolated atoms in each processor domain, `atomap_num_lg`, which is the number of local AND ghost interpolated atoms in each processor domain, and `atomap_num_lr`, which is the actual size of the second dimension of some `atomap`-related arrays. 

The differences between `atomap_num_l`, `atomap_num_lg`, and `atomap_num_lr`, as well as their relation with some `atomap`-related arrays are similar to those of `atom`-related variables and arrays, except that two other subroutines, `processor_scatter_cg.f90` and `processor_ghost_cg.f90`, are involved.

### Remark

In PyCAC, arrays for the atomistic domain, e.g., `atom`-related arrays, and those for the coarse-grained domain, e.g., `atomap`-related, `node`-related, and `ele`-related arrays, are completely separated. Take the position vector as an example, a processor may simultaneously have a `r_atom` array and a `r_atomap` array, yet it only has a `r_atom` or a `r_atomap` array if the system only contains real or interpolated atoms, i.e., fully atomistic or fully coarse-grained models. If one wants to add an additional array to the atomistic domain, e.g., to distinguish between different types of real atoms, one almost always has to also add a similar array to the coarse-grained domain to  distinguish different types of interpolated atoms, nodes, and elements.