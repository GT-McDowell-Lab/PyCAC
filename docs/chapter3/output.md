## Output

### A series of vtk and dump files created on-the-fly

The main output of a CAC simulation contains two types of files, with information of the elements, nodes, and atoms. In these files, `#`, a non-negative integer, is the simulation step at which a file is created:

* `cac_cg_#.vtk` and `cac_atom_#.vtk` files, created by `vtk_legacy.f90` and read by [ParaView](../chapter6/paraview.md), contain elemental/nodal information and atomic information in the coarse-grained and atomistic domains, respectively. Note that besides the nodal/atomic positions, the energy scalar, force vector, and stress tensor of each node/atom is also recorded in these `*.vtk` files. 
* `dump.#` files, created by `atomp_plot.f90` and read by [OVITO](../chapter6/ovito.md), are standard [LAMMPS dump files](http://lammps.sandia.gov/doc/dump.html) containing postions of the real atoms in the atomistic domain and the interpolated atoms in the coarse-grained domain. Each file can be [read by LAMMPS](http://lammps.sandia.gov/doc/read_dump.html) to carry out an equivalent fully-resolved atomistic simulation.

### One-time vtk and dump files 

Besides these files that are created on-the-fly (with a frequency of [`output_freq`](../chapter5/dump.md)), in the beginning of a simulation, a `model_atom.vtk` file containing atomic positions in the atomistic domain, a `model_cg.vtk` file containing nodal positions in the coarse-grained domain, and a `model_intpo.vtk` file containing integration point positions and weights in the coarse-grained domain are also created, by `vtk_legacy_model.f90`. A `dump.lammps` file which, in addition to the nodal/atomic positions, also contain the nodal/atomic velocities if [`simulation_style`](../chapter5/simulator.md) = _dynamics_ or _hybrid_, is created by `atomp_plot_lammps.f90`. When the total number of [new group, restart group](../chapter5/group_num.md), and [boundary group](../chapter5/bd_group.md) > 0, multiple `group_cg_#.vtk` and `group_atom_#.vtk` files, where `#`, a positive integer, is the group ID, are created by `vtk_legacy_group.f90`. These files are used to show whether the initial simulation cell and group settings are correct. Different from the `cac_cg_#.vtk` and `cac_atom_#.vtk` files, the `*.vtk` files here do not contain the energy/force/stress information, but only the nodal/atomic positions.

All `*.vtk` and `dump.*` files are then [post-processed](../chapter6/README.md) for visualization purposes.

### Other files

`cac.log` is the log file of a CAC simulation, containing information mostly written by `cac_log.f90`.

`stress_strain` and `temperature`, with a frequency of [`log_freq`](../chapter5/dump.md), record the $$3\times 3$$ stress/strain tensors and the temperature, respectively, at each [simulation step](../chapter5/run.md).

If [`boolean_debug`](../chapter5/debug.md) = _t_, a writable `debug` file is created by `debug_init.f90`. The user can then write to it whatever he/she wants using unit number 13, i.e.,

	write(13, format) output

When the total number of [new group, restart group](../chapter5/group_num.md), and [boundary group](../chapter5/bd_group.md) > 0, a series of `group_out_#.id` files are created, where `#` is a postive integer starting from 1. These files can then be renamed to `group_in_#.id` for [restart group](../chapter5/group.md) and [refinement](../chapter5/refine.md) purposes.

A series of `cac_out_#.restart files` are also created, where `#` is a positive integer starting from 1. One of these files can then be renamed to `cac_in.restart` to restart a previous simulation when [boolean_restart](../chapter5/restart.md) = _t_.