## deform

### Syntax

	deform boolean_def def_num
	       {ij boolean_cg boolean_at def_rate stress_l stress_u flip_frequency}
	       time time_start time_always_flip time_end 

* `boolean_def`, `boolean_cg`, `boolean_at` = _t_ or _f_

		t is true
		f is false

* `def_num` = non-negative integer (<= 9)

* `ij` = _xx_ or _yy_ or _zz_ or _xy_ or _yz_ or _yz_ or _zy_ or _xz_ or _zx_

* `def_rate` = real number

* `stress_l`, `stress_u` = positive real number

* `flip_frequency` = positive integer

* `time_start`, `time_always_flip`, `time_end` = non-negative integer

### Examples

	deform t 1 {zx t t 0.05 0.6 0.7 10} time 500 1000 2500
	deform t 2 {xx t f 0.01 1. 1.2 20} {yz f t 0.02 0.8 0.9 30} time 400 600 1900

### Description

This command sets up the homogeneous deformation of the simulation cell. Note that the curly brackets `{` and `}` in the syntax/examples are to separate different deformation modes, the number of which is `def_num`; all brackets should not be included in preparing `cac.in`.

The deformation is applied only if `boolean_def` = _t_. The coarse-grained and atomistic domains are deformed only if `boolean_cg` and `boolean_at` are _t_, respectively.

`def_num` sets the number of superimposed deformation modes.

`ij` decides each deformation mode, i.e., how the strain is applied. Following the standard indexes $$\epsilon_{ij}$$ in continuum mechanics, `i` and `j` are the face on which and the direction along which the strain is applied. When `i` and `j` are the same, a uniaxial strain is applied; otherwise, a shear strain is applied.

`def_rate` is the strain rate, in ps$$^{-1}$$.

`stress_l` and `stress_u` are the lower and upper bounds of the stress tensor component (designated by `ij`) of the simulation cell, respectively, in GPa. In CAC simulations, all stress components are usually small at the beginning. Subject to the strain, most stress tensor components increase in magnitude until one of them is higher than the corresponding `stress_u`, at which point the strain rate tensor changes sign, i.e., the deformation is reversed but each `ij` remains unchanged. Subject to the newly reversed strain, most stress tensor components decrease until one of them is lower than the corresponding `stress_l`, in which case the strain rate tensor changes sign again, i.e., the deformation is applied as the initial setting. Whether the stress component is out of bounds is monitored not at every step, but at every `flip_frequency` step.

The deformation begins when the [simulation step](run.md) equals `time_start` and stops when it exceeds `time_end`.

When (i) the [simulation step](run.md) is larger than `time_always_flip` and (ii) the [simulation step](run.md) does not exceed `time_end` and (iii) the strain rate tensor did not change sign previously, the strain rate tensor changes sign at every step, regardless of the stress bounds defined by `stress_l` and `stress_u`. This is used, e.g., to keep a quasi-constant strain while the nodes and atoms adjust their positions in dynamic or quasistatic equilibrium. To disable this option, the user may set `time_always_flip` to be larger than `time_end`.

### Related commands

Groups defined by the [bd_group](bd_group.md) and [group](group.md) commands may be homogeneously deformed along with the simulation cell, depending on the value of `boolean_def` in these two commands.

### Related files

`deform_init.f90` and `deform_box.f90`

### Default

	deform f 1 xx f f 0. 0. 0. 1 time 0 0 0

