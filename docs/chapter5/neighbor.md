## neighbor

### Syntax

	neighbor bin_size update_neighbor_freq

* bin\_size = real number

* update\_neighbor\_freq = integer

### Examples

	neighbor 1. 100
	neighbor 2. 200

### Description

Set parameters for atomic neighbors.

`bin_size`, in unit of Angstrom, sets the length of the bin, which adds to the cutoff radius of the interatomic potential. All atoms within the distance of interatomic potential cutoff + bin\_size from an atom are the neighbors of the latter atom.

`update_neighbor_freq` is the frequency at which the neighbor updator is issued. The updator will first check if, with respect to the atomic/nodal positions after the last check, any atom or node has a displacement larger than half the `bin_size`. If yes, all neighbors of all atoms/nodes/integration points are updated.

### Related commands

The number of neighbors per atom is set by the [limit](limit.md) command.

### Related files

`neighbor_init.f90` and `update_neighbor.f90`

### Default

	neighbor 1. 100