## potential

### Syntax

	potential potential_type cohesive_energy

* potential\_type = _lj_ or _eam_

		lj is the Lennard-Johns potential
		eam is the embedded-atom method potential

### Examples

	potential lj -3.54
	potential eam -4.45

### Description

Set the intertomic potential used in PyCAC simulations.

Currently, only two `potential_type` are allowed: the _lj_ potential and the _eam_ potential.

For the _lj_ potential, a `lj.para` file is required. It contains epsilon, sigma, minimum cutoff radius, and cutoff radius.

For the _eam_ potential, three files are required, including `edens.tab`, `pair.tab`, and `embed.tab`.

In `edens.tab`, the first column is the interatomic distance, in unit of Anstron, while the second one is the electronic density, in unit of XX.

In `pair.tab`, the first column is the interatomic distance, in unit of Anstrong, while the second one is the pair potential, in unit of eV.

In `embed.tab`, the first column is the host electronic density, in unit of XX, while the second one is the embedded energy, in unit of eV.

The `cohesive_energy` is the cohesive energy of one atom given by the interatomic potential, in unit of eV.

### Related commands

None.

### Related files

`potential.f90`, `eam_tab.f90`, and `lj_para.f90`, among many

### Default

None.