## dynamics

### Syntax

	dynamics dyn_style energy_min_freq damping coefficient

* dyn\_style = _ld_ or _qd_ or _vv_

		ld is Langevin dynamics
		qd is quenched dynamics
		vv is velocity Verlet

* energy\_min\_freq = integer

* damping coefficient = real number

### Examples

	dynamics ld 300 1.
	dynamics qd 500 5.

### Description

Set the style of dynamic run.

When dyn\_style = ld, the Langevin dynamics is set, following the [Langevin equation](https://en.wikipedia.org/wiki/Langevin_dynamics), where the $$\gamma$$ is the `damping coefficient`, in unit of XX. The algorithm in PyCAC is given in Eqs. 1-3 in [Xu et al., IJSS, 2016](). The ld style is used to control temperature in PyCAC.

When dyn\_style = qd, the quenched dynamics is set. The algorithm in PyCAC is given in [Xu et al., npj Comput. Mater., 2016](). Note that with the qd style, the temperature is considered 0 K or very nearly so.

When dyn\_style = vv, dynamic simulation follows the velocity Verlet scheme. Note that the vv style cannot be use to control temperature.

The energy\_min\_freq is the frequency at which the energy minimization is performed during a dynamic run. This is relavant only if the [simulator](simulator.md) is `hybrid`.

### Related commands

[run](run.md) and [simulator](simulator.md).

### Related files

`dynamics_init.f90`, `dynamics.f90`, `langevin_dynamics.f90`, `quenched_dynamics.f90`, `hybrid.f90`, among many

### Default

	dynamics vv 500 1.
