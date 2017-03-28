## deform

### Syntax

	deform boolean_def def_num
	       ij boolean_cg boolean_at def_rate stress_l stress_u flip_frequency
	       time time_start time_always_flip time_end 

* boolean\_def, boolean\_cg, boolean\_at = _t_ or _f_

		t is true
		f is false

* def\_num = integer (<= 9)

* ij = _xx_ or _yy_ or _zz_ or _xy_ or _yz_ or _yz_ or _zy_ or _xz_ or _zx_

* def\_rate, stress\_l, stress\_u = real number

* flip\_frequency, time\_start, time\_always\_flip, time\_end = integer

### Examples

	deform t 1 zx t t 0.05 0.6 0.7 10 time 500 1000 2500
	deform t 2 xx t f 0.01 1. 1.2 20 yz f t 0.02 0.8 0.9 30 time 400 600 1900

### Description

Set up the homogeneous deformation of the whole simulation box. The deformation is underway if `boolean_def` is t.

`def_num` defines how many deformation matrix is added. When `def_num` > 1, all deformation matrices are linearly superimposed.

`ij` decides how the strain is applied. Following the standard indexes in continuum mechanics, `i` and `j` are the face on which and the direction along which the strain is applied. When `i` and `j` are the same, a uniaxial strain is set, otherwise, a shear strain is set.

`def_rate` is the strain rate, in the unit of ps$$^{-1}$$.

`stress_l` and `stress_u` are the lower and upper bounds of the applied stress, respectively, for the stress tensor component specified by `ij`, in unit of GPa. Assume that all stress components are initially zero or very small. Then when the stress component is higher than `stress_u`, the corresponding strain rate changes sign, i.e., the deformation is reversed. Afterward, when the stress component is lower than `stress_l`, the corresponding strain rate changes sign again, i.e., the deformation proceeds as the initial setting. Whether the stress component is out of the bounds is checked not every step, but at every `flip_frequency` step.

The deformation begins after time step `time_start` and ends after `time_end`. When the time step is larger than `time_always_flip` but smaller than `time_end`, the strain rate changes sign at every step back and forth, regardless of the stress bounds defined by `stress_l` and `stress_u`.

### Related commands

Groups defined by the [group](group.md) and [bd_group](bd_group.md) commands may be homogeneous deformed along with the simulation cell, depending on settings in those two commands.

### Related files

`deform_init.f90` and `deform_box.f90`

### Default

`boolean_def` = f.

