## neighbor

### Syntax

	neighbor bin_size neighbor_freq

* `bin_size` = non-negative real number

* `neighbor_freq` = positive integer

### Examples

	neighbor 1. 100
	neighbor 2. 200

### Description

This command sets parameters for updating the neighbor list. In CAC simulatoins, each atom in the atomistic domain and each integration point in the coarse-grained domain maintain neighbor lists. Note that the non-integration point interpolated atoms in the coarse-grained domain do not maintain neighbor lists because their force/energy etc. are not calculated.

`bin_size`, in unit of Angstrom, sets the length of the bin, which adds to the cutoff distance $$r_\mathrm{c}$$ of the [interatomic potential](potential.md). All atoms within [cutoff distance](../chapter3/input.md) + `bin_size` from an atom/integration point are the neighbors of this atom.

`neighbor_freq` is the frequency with which a check of whether the neighbor list should be updated is conducted. The neighbor lists of all atoms/integration points are updated if, with respect to the nodal/atomic positions recorded at the last check, any node or atom has a displacement larger than half the `bin_size`.

### Related commands

The initial number of neighboring atoms per atom/integration point is set in the [limit](limit.md) command.

### Related files

`neighbor_init.f90` and `update_neighbor.f90`

### Default

	neighbor 1. 200