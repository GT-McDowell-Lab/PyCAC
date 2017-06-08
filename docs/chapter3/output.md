## Output

`cac.log` is the log file of a CAC simulation, containing information mostly output by `cac_log.f90`.

`stress_strain` records the $$3\times 3$$ stress tensor followed by the $$3\times 3$$ strain tensor at each simulation step.

If _debug_ is set to true in `cac.in`, a `debug` file is created by `debug_init.f90`.

Two types of files are created carrying information of the elements, nodes, and atoms:

* `cac_cg_*.vtk` and `cac_atom_*.vtk` files, read by [ParaView](../chapter6/paraview.md), contain elemental/nodal information and atomic information in the coarse-grained and atomistic domains, respectively. The files are created by `vtk_legacy.f90`.
* `dump.*` files, read by [OVITO](../chapter6/ovito.md), are standard [LAMMPS dump files](http://lammps.sandia.gov/doc/dump.html). The files are created by `atomp_plot.f90`.

In these files, the `*` is the simulation step at which a file is created.

Besides, at the beginning of a simulation (`model.f90`), a `dump.lammps` file that can be [read by LAMMPS](http://lammps.sandia.gov/doc/read_dump.html) to carry out equivalent fully-resolved atomistic simulations, a `model_atom.vtk` file containing atomic positions in the atomistic domain, a `model_cg.vtk` file containing nodal positions in the coarse-grained domain, and a `model_intpo.vtk` file containing integration point positions and weights in the coarse-grained domain. These files are created by `atomp_plot_lammps.f90` and `vtk_legacy_model.f90`.

All `*.vtk` and `dump.*` files are then [post-processed](../chapter6/README.md) for visualization purposes.