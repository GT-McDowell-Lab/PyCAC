## limit

### Syntax

	limit atom_per_cell_number atomic_neighbor_number

* `atom_per_cell_number`, `atomic_neighbor_number` = integer

### Examples

	limit 100 100
	limit 120 140

### Description

Set the initial limitations of the number of atoms per cell and the number of neighboring atoms per atom. The numbers, often given based on experiences, are used to allocate large enough arrays for cell and atomic neighbors. If the real numbers become larger than these initial limitations during the simulation, the limitations will increase in increments of 20, until the real numbers are once again larger than the new limitations.

### Related commands

These limitations mainly depend on the `lattice_constant` in the [lattice](lattice.md) command, the cutoff radius of the [interatomic potential](here.md), and the `bin_size` in the [neighbor](neighbor.md) command.

### Related files

`neighbor_init.f90`, `update_neighbor.f90`, `cell_neighbor_list.f90`, `update_cell_neighbor.f90`, and `update_cell.f90`

### Default

	limit 100 100