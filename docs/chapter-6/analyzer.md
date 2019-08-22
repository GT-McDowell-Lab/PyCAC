
A data analyzer is provided in the `analyzer` directory.

### vtk2dump

A file `vtk2dump.f90` is provided in the directory `analyzer/vtk2dump` to convert at most two `*.vtk` files to a `dump.*` file. To compile it, simply

	ifort vtk2dump.f90 -o vtk2dump

or

	gfortran vtk2dump.f90 -o vtk2dump

To run the code, simply

	./vtk2dump

The executable then reads at most three files, namely, `cac_cg_#.vtk`, `cac_atom_#.vtk`, and `vtk2dump.in`. From `cac_cg_#.vtk`, the atomic positions inside the elements are linearly interpolated from the nodes; from `cac_atom_#.vtk`, the atomic positions are read as is. Then both interpolated atoms and real atoms are written into a `dump.#` file. Here, `#`, a positive integer, is provided by the `step` in the `vtk2dump.in` file, whose syntax is

	boolean_cg boolean_at
	step
	x boolean_user lower_b upper_b
	y boolean_user lower_b upper_b
	z boolean_user lower_b upper_b

* `boolean_cg`, `boolean_at`, `boolean_user` = _t_ or _f_

* `x`, `y`, `z` = _p_ or _s_

* `lower_b`, `upper_b` = real number

For example,

	t t
	34
	p t 0. 100.
	s f
	p f -50. 150.

`boolean_cg` and `boolean_at` decide whether the files `cac_cg_#.vtk` and `cac_atom_#.vtk` are involved in the conversion, respectively. For example, if `boolean_cg` = _t_ and `boolean_at` = _f_, only `cac_cg_#.vtk` is converted.

In the example, `step` = 34, meaning that files `cac_cg_34.vtk` and/or `cac_atom_34.vtk` should be prepared, and the output file is `dump.34`.

`x`, `y`, and `z` set the [boundary conditions](../chapter-5/boundary.md) along the _x_, _y_, and _z_ directions, respectively.

If `boolean_user` = _t_, it should be followed by `lower_b` and `upper_b`, in units of Angstrom, which provide user-defined lower and upper bounds of the simulation cell along the corresponding direction. If `boolean_user` = _f_, `lower_b` and `upper_b`, e.g., `-50.` and `150.` in the last line of the example, become irrelevant; in this case, the two bounds along a certain direction are calculated using the nodal and atomic positions in the two `*.vtk` files.