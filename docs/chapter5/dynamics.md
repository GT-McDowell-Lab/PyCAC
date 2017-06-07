## dynamics

### Syntax

	dynamics dyn_style energy_min_freq damping_coefficient

* `dyn_style` = _ld_ or _qd_ or _vv_

		ld is Langevin dynamics
		qd is quenched dynamics
		vv is velocity Verlet

* `energy_min_freq` = positive integer

* `damping_coefficient` = positive real number

### Examples

	dynamics ld 300 1.
	dynamics qd 500 5.

### Description

This command sets the style of dynamic run in PyCAC simulations.

When `dyn_style` = _ld_, the [Langevin dynamics](https://en.wikipedia.org/wiki/Langevin_dynamics) is performed, i.e.,

$$m \ddot{\mathbf{R}} = \mathbf{F} - \gamma \dot{\mathbf{R}}$$

where $$m$$ is the normalized lumped mass or the atomic mass, $$\mathbf{R}$$ is the nodal/atomic position, $$\mathbf{F}$$ is the equivalent nodal/atomic force, and $$\gamma$$ is the `damping_coefficient`, in unit of ps$$^{-1}$$. In the PyCAC code, the Velocity Verlet form is employed, as given in Eqs. 1-3 in [Xu et al., 2016](http://dx.doi.org/10.1016/j.ijsolstr.2016.03.030). The velocity $$\dot{\mathbf{R}}$$ is updated in `langevin_vel.f90`.

Note that the _ld_ style is used to keep a constant temperature in PyCAC simulations by adding to the force a normal random variable with the mean zero and the deviation $$\sqrt{2m\gamma k_\mathrm{B} T/\Delta t}$$, where $$m$$ is the atomic mass, $$k_\mathrm{B}$$ is the Boltzmann constant ($$8.6173324\times 10^{-5} \mathrm{eV/K}$$), $$T$$ is the temperature in unit of K, and $$\Delta t$$ is the [time step](run.md) in unit of ps. The random variable is calculated and added to the force in `langevin_force.f90`.

When `dyn_style` = _qd_, the quenched dynamics is performed, in which

* if the force and velocity point in opposite directions, the velocity is zeroed, i.e.,

$$\mathrm{if}\ \dot{\mathbf{R}} \cdot \mathbf{F} < 0, \dot{\mathbf{R}} = 0$$

* otherwise, the velocity is projected along the direction of the force, such that only the component of velocity parallel to the force vector is used, i.e.,

$$\mathrm{if}\ \dot{\mathbf{R}} \cdot \mathbf{F} \geq 0, \dot{\mathbf{R}} = \frac{(\dot{\mathbf{R}} \cdot \mathbf{F})\mathbf{F}}{|\mathbf{F}|^2}$$

Note that with the _qd_ style, which was first used in [Xu et al., 2016](http://dx.doi.org/10.1038/npjcompumats.2015.16), the temperature is considered 0 K or very nearly so.

When `dyn_style` = _vv_, dynamic simulation follows the Velocity Verlet scheme. Note that the _vv_ style cannot be used to keep a constant temperature; a warning will be issued if the user tries to do so.

The `energy_min_freq` is the frequency with which the energy minimization is performed during a dynamic run. This is relevant only if the [simulator_type](simulator.md) is `hybrid`.

### Related commands

[run](run.md) and [simulator](simulator.md).

### Related files

`dynamics_init.f90`, `dynamics.f90`, `langevin_dynamics.f90`, `quenched_dynamics.f90`, `hybrid.f90`, among many

### Default

	dynamics vv 500 1.