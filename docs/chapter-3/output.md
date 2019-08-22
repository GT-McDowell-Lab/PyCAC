### A series of vtk files created on-the-fly

The main output of a CAC simulation are `cac_cg_#.vtk` and `cac_atom_#.vtk` files that contain elemental/nodal information and atomic information in the coarse-grained and the atomistic domains, respectively, where `#`, a non-negative integer, is the simulation step at which the file is created. These files, created by `vtk_legacy.f90` with a frequency of [`output_freq`](../chapter-5/dump.md), can be read by [ParaView](../chapter-6/paraview.md). Note that besides the nodal/atomic positions, the energy scalar, the force vector, and the stress tensor of each node/atom are also recorded in these vtk files.

### One-time vtk and dump files 

Besides the files that are created on-the-fly, in the beginning of a simulation, a `model_atom.vtk` file containing atomic positions in the atomistic domain, a `model_cg.vtk` file containing nodal positions in the coarse-grained domain, and a `model_intpo.vtk` file containing integration point positions and weights in the coarse-grained domain are also created, by `vtk_legacy_model.f90`. A standard [LAMMPS dump](http://lammps.sandia.gov/doc/dump.html) file `dump.lammps` which, in addition to the positions of the real/interpolated atoms, also contain the velocities of the real/interpolated atoms if [`simulation_style`](../chapter-5/simulator.md) = _dynamics_ or _hybrid_, is created by `atomp_plot_lammps.f90`. When the [total number of groups](../chapter-5/group_num.md) > 0, multiple `group_cg_*.vtk` and `group_atom_*.vtk` files, where `*`, a positive integer, is the group id, are created by `vtk_legacy_group.f90` for the coarse-grained and the atomistic domains, respectively. These files are used to show whether the initial simulation cell and group settings are correct. Different from the `cac_cg_#.vtk` and `cac_atom_#.vtk` files, the one-time vtk files here do not contain the energy/force/stress information, but only the nodal/atomic positions.

All vtk and dump files are then [post-processed](../chapter-6/README.md) for visualization purposes.

### Other files

`cac.log` is the log file of a CAC simulation, containing information mostly written by `cac_log.f90`.

`stress_strain` and `temperature`, with a frequency of [`log_freq`](../chapter-5/dump.md), record the $3\times 3$ stress/strain tensors and the temperature, respectively, at certain [simulation step](../chapter-5/run.md).

A series of `cac_out_#.restart` files, where `#` is a positive integer, are created with a frequency of [`restart_freq`](../chapter-5/dump.md). One of these files can then be renamed to `cac_in.restart` to restart a prior simulation when [boolean_restart](../chapter-5/restart.md) = _t_.

If [`boolean_debug`](../chapter-5/debug.md) = _t_, a writable `debug` file is created by `debug_init.f90`. The user can then write to it whatever he/she wants using unit number 13, i.e.,

	write(13, format) output

When the [total number of groups](../chapter-5/group_num.md) > 0, a series of `group_out_*_#.id` files are created, where `*` is the group id starting from 1 and `#` is the simulation step at which the file is created. These files can then be renamed to `group_in_*.id` for [restart group](../chapter-5/group_num.md) and [refinement](../chapter-5/refine.md) purposes.