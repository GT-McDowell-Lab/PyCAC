## neighbor

### Syntax

	neighbor bin_size neighbor_freq

* `bin_size` = non-negative real number

* `neighbor_freq` = positive integer

### Examples

	neighbor 1. 100
	neighbor 2. 200

### Description

This command sets parameters for updating the neighbor list. In PyCAC simulatoins, each atom in the atomistic domain and each integration point in the coarse-grained domain maintain neighbor lists. Note that the non-integration point interpolated atoms in the coarse-grained domain do not have neighbor lists.

`bin_size`, in unit of Angstrom, sets the length of the bin, which adds to the cutoff distance $$r_\mathrm{c}$$ of the [interatomic potential](potential.md). All atoms within [cutoff distance](../chapter3/input.md) + `bin_size` from an atom are the neighbors of this atom.

`neighbor_freq` is the frequency with which a check of whether the neighbor list should be updated is issued. The neighbor list is updated if, with respect to the nodal/atomic positions recorded at the last check, any node or atom has a displacement larger than half the `bin_size`. If yes, all neighbors of all atoms/nodes/integration points are updated.

### Related commands

The number of neighbors per atom is set by the [limit](limit.md) command.

### Related files

`neighbor_init.f90` and `update_neighbor.f90`

### Default

	neighbor 1. 200