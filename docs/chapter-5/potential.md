
### Syntax

	potential potential_type

* `potential_type` = _lj_ or _eam_

		lj is the Lennard-Johns potential
		eam is the embedded-atom method potential

### Examples

	potential lj
	potential eam 

### Description

This command sets the interatomic potentials. Currently, a CAC simulation accepts two `potential_style`: Lennard-Johns (_lj_) and embedded-atom method (_eam_) potentials. [One file for the _lj_ potential and four files for the _eam_ potential](../chapter-3/input.md), respectively, should be provided as input.

### Related commands

None.

### Related files

`potential.f90`, `eam_tab.f90`, `deriv_tab.f90`, and `lj_para.f90`.

### Default

None.
