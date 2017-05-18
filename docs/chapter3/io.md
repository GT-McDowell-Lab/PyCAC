## Input/Output

### Input

The [commands](../chapter5/README.md) in the `cac.in` file provide most of what are required for a PyCAC simulation. Besides, one needs to provide potential files: `embed.tab`, `pair.tab`, and `edens.tab` for the EAM potential; `lj.para` for the LJ potential.

For the EAM potentials, the first line of 

The format 

### Output

`cac.log`

`cac_cg_*.vtk` and `cac_atom_*.vtk` files are read by

`stress_strain` post-processed by gnuplot, etc.