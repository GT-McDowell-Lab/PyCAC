## limit

### Syntax

	limit atom_per_cell_number atomic_neighbor_number

* `atom_per_cell_number`, `atomic_neighbor_number` = positive integer

### Examples

	limit 100 100
	limit 120 140

### Description

This command sets the initial number of atoms per cell (`atom_per_cell_number`) and the number of neighboring atoms per atom/integration point (`atomic_neighbor_number`). The numbers are used to allocate initial arrays for atoms in cells and neighbors of atoms/integration points. If, during a simulation, arrays larger than those initially allocated become necessary, the two numbers set in this command will increase by 20 to enlarge the arrays, until even larger arrays are needed, in which case these two numbers increase by 20 again, and so on.

### Related commands

The initial values of these two numbers depend on the [cutoff distance $$r_\mathrm{c}$$](../chapter3/input.md) and [bin_size](neighbor.md) of the [interatomic potential](potential.md).

### Related files

`neighbor_init.f90`, `update_neighbor.f90`, `cell_neighbor_list.f90`, `update_cell_neighbor.f90`, and `update_cell.f90`

### Default

	limit 100 100